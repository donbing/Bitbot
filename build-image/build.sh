#!/bin/bash
# build.sh: Use pi-gen (Docker) to build a custom Raspberry Pi OS image with Docker and Bitbot
set -e

# Clone pi-gen if not present
if [ ! -d pi-gen ]; then
  git clone --depth 1 https://github.com/RPi-Distro/pi-gen.git pi-gen
fi

# Copy custom Bitbot stage into pi-gen
rm -rf pi-gen/stage-bitbot
cp -r stage-bitbot pi-gen/

# Copy Bitbot project into stage files
rm -rf stage-bitbot/files/bitbot
mkdir -p stage-bitbot/files/bitbot
rsync -a --exclude 'build-image' --exclude '.git' ../../ stage-bitbot/files/bitbot/

# Ensure pi-gen config exists
if [ ! -f pi-gen/config ]; then
  echo "IMG_NAME='bitbot-pi'" > pi-gen/config
fi

# Add custom stage to build config if not present
if ! grep -q 'stage-bitbot' pi-gen/config; then
  echo "STAGE_LIST='stage0 stage1 stage2 stage-bitbot'" >> pi-gen/config
fi

# Build the image using Docker
cd pi-gen
./build-docker.sh

# Move the final image to output directory
cd ..
mkdir -p output
find pi-gen/deploy -name '*.img' -exec cp {} output/bitbot-pi.img \;

echo "Image ready: output/bitbot-pi.img"

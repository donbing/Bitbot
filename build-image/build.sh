#!/bin/bash
# build.sh: Use pi-gen to build a custom Raspberry Pi OS image with Docker and Bitbot
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

# Add custom stage to build config
if ! grep -q '^STAGE_LIST=.*stage-bitbot' pi-gen/config; then
  sed -i 's/^STAGE_LIST=.*/& stage-bitbot/' pi-gen/config
fi

# Build the image
cd pi-gen
sudo ./build.sh

# Move the final image to output directory
cd ..
mkdir -p output
find pi-gen/deploy -name '*.img' -exec cp {} output/bitbot-pi.img \;

echo "Image ready: output/bitbot-pi.img"

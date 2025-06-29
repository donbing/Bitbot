#!/bin/bash
# build.sh: Build a minimal Raspberry Pi OS image with Docker and Bitbot Docker Compose
set -e

IMG=output/bitbot-pi.img
IMG_SIZE=4G
MOUNT_DIR=mnt

# Clean up previous build
sudo umount -lf $MOUNT_DIR || true
rm -rf $MOUNT_DIR output
mkdir -p $MOUNT_DIR output

# Download minimal Raspberry Pi OS Lite image
wget -O output/rpi-os-lite.img https://downloads.raspberrypi.com/raspios_lite_armhf_latest

# Extract the image
mv output/rpi-os-lite.img $IMG

# Mount the image
LOOPDEV=$(sudo losetup -f --show $IMG)
PART=$(sudo kpartx -av $LOOPDEV | grep -m1 'p2' | awk '{print $3}')
sudo mount /dev/mapper/$PART $MOUNT_DIR

# Copy Bitbot project and Docker Compose files
sudo mkdir -p $MOUNT_DIR/home/pi/bitbot
sudo rsync -a --exclude 'build-image' --exclude '.git' ../../ $MOUNT_DIR/home/pi/bitbot/

# Install Docker and Docker Compose on first boot
cat <<'EOF' | sudo tee $MOUNT_DIR/etc/rc.local > /dev/null
#!/bin/bash
# rc.local
set -e
if ! command -v docker &> /dev/null; then
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  usermod -aG docker pi
fi
if ! command -v docker-compose &> /dev/null; then
  pip3 install docker-compose
fi
cd /home/pi/bitbot
/usr/local/bin/docker-compose up -d
exit 0
EOF
sudo chmod +x $MOUNT_DIR/etc/rc.local

# Unmount and clean up
sudo umount $MOUNT_DIR
sudo kpartx -d $LOOPDEV
sudo losetup -d $LOOPDEV

echo "Image ready: $IMG"

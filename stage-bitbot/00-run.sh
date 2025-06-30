#!/bin/bash
# 00-run.sh: Install Docker, Docker Compose, and Bitbot files
set -e

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker pi

# Install Docker Compose
pip3 install docker-compose

# Copy Bitbot project (assumes /stage-bitbot/files/bitbot exists)
mkdir -p /home/pi/bitbot
cp -r /stage-bitbot/files/bitbot/* /home/pi/bitbot/
chown -R pi:pi /home/pi/bitbot

# Enable Docker Compose on boot
cat <<'EOF' > /etc/rc.local
#!/bin/bash
set -e
cd /home/pi/bitbot
/usr/local/bin/docker-compose up -d
exit 0
EOF
chmod +x /etc/rc.local

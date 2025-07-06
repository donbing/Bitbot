#!/bin/bash -e

# Install Docker Compose if not present (for legacy systems)
if ! command -v docker-compose &>/dev/null && ! docker compose version &>/dev/null; then
    apt-get update
    apt-get install -y docker-compose
fi

# Add the pi user to the docker group
usermod -aG docker "$FIRST_USER_NAME"

# Create target directory for compose files
mkdir -p /opt/bitbot

# Copy docker-compose files from stage to image (if present)
if [ -f docker-compose.yml ]; then
    cp docker-compose.yml /opt/bitbot/
fi

# Create systemd service for docker compose
cat > /etc/systemd/system/bitbot-compose.service <<EOL
[Unit]
Description=Bitbot Docker Compose Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/bitbot
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
EOL

# Enable the service
systemctl enable bitbot-compose.service

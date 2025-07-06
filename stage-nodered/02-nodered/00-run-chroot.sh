#!/bin/bash -e

# based on https://github.com/Tknika/iombian/blob/master/stage9/05-node-red/00-run-chroot.sh

NODERED_VERSION=4.0.5

NODERED_USER=$FIRST_USER_NAME
NODERED_GROUP=$FIRST_USER_NAME
NODERED_HOME=$( getent passwd "$NODERED_USER" | cut -d: -f6 )

# install node-red package
npm i -g --unsafe-perm --no-progress node-red@$NODERED_VERSION

# set local folder
mkdir -p "$NODERED_HOME/.node-red/node_modules"
chown -Rf $NODERED_USER:$NODERED_GROUP $NODERED_HOME/.node-red/
pushd "$NODERED_HOME/.node-red"
npm config set update-notifier false

# create package.json
if [ ! -f "package.json" ]; then
    echo '{' > package.json
    echo '  "name": "node-red-project",' >> package.json
    echo '  "description": "A Node-RED Project",' >> package.json
    echo '  "version": "0.0.1",' >> package.json
    echo '  "dependencies": {' >> package.json
    echo '  }' >> package.json
    echo '}' >> package.json
fi

# install bcryptjs library
npm i --unsafe-perm --save --no-progress bcryptjs

# install extra Pi nodes
EXTRANODES="node-red-dashboard"
npm i --unsafe-perm --save --no-progress $EXTRANODES

# reset permissions
popd
mkdir -p "$NODERED_HOME/.npm"
chown -Rf $NODERED_USER:$NODERED_GROUP $NODERED_HOME/.npm
chown -Rf $NODERED_USER:$NODERED_GROUP $NODERED_HOME/.node-red/

# start/stop/log scripts
mkdir -p /usr/bin
curl -sL -o /usr/bin/node-red-start https://raw.githubusercontent.com/node-red/linux-installers/master/resources/node-red-start
curl -sL -o /usr/bin/node-red-stop https://raw.githubusercontent.com/node-red/linux-installers/master/resources/node-red-stop
curl -sL -o /usr/bin/node-red-restart https://raw.githubusercontent.com/node-red/linux-installers/master/resources/node-red-restart
curl -sL -o /usr/bin/node-red-reload https://raw.githubusercontent.com/node-red/linux-installers/master/resources/node-red-reload
curl -sL -o /usr/bin/node-red-log https://raw.githubusercontent.com/node-red/linux-installers/master/resources/node-red-log
curl -sL -o /etc/logrotate.d/nodered https://raw.githubusercontent.com/node-red/linux-installers/master/resources/nodered.rotate
chmod +x /usr/bin/node-red-start
chmod +x /usr/bin/node-red-stop
chmod +x /usr/bin/node-red-restart
chmod +x /usr/bin/node-red-reload
chmod +x /usr/bin/node-red-log

# add systemd script
curl -sL -o /lib/systemd/system/nodered.service https://raw.githubusercontent.com/node-red/linux-installers/master/resources/nodered.service
sed -i 's#^User=pi#User='$NODERED_USER'#;s#^Group=pi#Group='$NODERED_GROUP'#;s#^WorkingDirectory=/home/pi#WorkingDirectory='$NODERED_HOME'#;' /lib/systemd/system/nodered.service

# remove unneeded large sentiment library to save space and load time
rm -f /usr/lib/node_modules/node-red/node_modules/multilang-sentiment/build/output/build-all.json

# enable systemd service
systemctl enable nodered.service
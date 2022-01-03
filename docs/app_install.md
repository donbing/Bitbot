
# Setup Options

## Burn the Bitbot image to a new SD card
---
> Simple installation that anyone can complete
1. download the latest release from [releases page](https://github.com/donbing/bitbot/releases)  
2. use [Balena Etcher](https://www.balena.io/etcher/) to burn the zipped image to your SD card.

## Add to an existing PiOS install ]
> note I've been  unable to get this working on bullseye so-far
---
> For advanced users that want to modify an existing pi
1. Install Git, Pip (plus some dependencies)
```sh
sudo apt-get install git python3-pip libffi-dev libtiff5 libjpeg62 libopenjp2-7-dev libatlas-base-dev
curl https://get.pimoroni.com/inky | bash
```  
2. optionally Install [wifi connection helper](https://github.com/jasbur/RaspiWiFi)
```sh
git clone https://github.com/jasbur/RaspiWiFi
cd RaspiWiFi
sudo python3 initial_setup.py
```
3. Clone this repo and setup requirements
```sh
git clone https://github.com/donbing/bitbot
cd bitbot 
pip3 install --user -r requirements.txt --index-url=https://www.piwheels.org/simple/
```
4. Add cron jobs for screen refresh intervals
```sh
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && python3 /home/pi/bitbot/run.py 2>&1 | /usr/bin/logger -t bitbot")| crontab -
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && python3 /home/pi/bitbot/src/config_webserver.py 2>&1 | /usr/bin/logger -t bitbot")| crontab -
```
5. Test the app 
```sh
python3 -m run
```

## Install in docker
> Highly flexible approach that allows for simple updates
---
1. ensure that `I2C`/`SPI` are enabled on the host pi
```sh
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
```
2. run the container
```sh
docker run --privileged -d ghcr.io/donbing/bitbot:release
```

> Debug log
```sh
tail ~/bitbot/debug.log
# or
more /var/log/syslog | grep bitbot
```

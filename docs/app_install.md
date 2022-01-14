# Setup Options

## A. Burn the Bitbot image to a new SD card
---
> Simple installation that anyone can complete
1. download the latest release from [releases page](https://github.com/donbing/bitbot/releases)  
2. use [Balena Etcher](https://www.balena.io/etcher/) to burn the zipped image to your SD card.
3. insert SD, power up and wait for the screen to refresh
## B. Add to an existing PiOS install
> For advanced users that want to modify an existing pi

> Note: I've been  unable to get this working on bullseye so-far, only the legacy buster image  

1. make sure python, pip, git and other dependancies are installed
```sh
sudo apt update -y
sudo apt install -y git python3-pip python3-matplotlib python3-rpi.gpio python3-pil
```  
2. Clone this repo and setup requirements
```sh
git clone https://github.com/donbing/bitbot
cd bitbot 
pip3 install --user -r requirements.txt
```
3. Add cron jobs to start the app and config server
```sh
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && python3 /home/pi/bitbot/run.py 2>&1 | /usr/bin/logger -t bitbot")| crontab -
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && python3 /home/pi/bitbot/src/config_webserver.py 2>&1 | /usr/bin/logger -t bitbot")| crontab -
```
4. ensure that `I2C`/`SPI` are enabled on the host pi
```sh
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
```
5. Test the app 
```sh
python3 -m run
```
6. optionally Install [wifi connection helper](https://github.com/jasbur/RaspiWiFi)
```sh
git clone https://github.com/jasbur/RaspiWiFi
cd RaspiWiFi
sudo python3 initial_setup.py
```
## C. Install in docker
> Highly flexible approach that allows for simple updates
1. ensure that `I2C`/`SPI` are enabled on the host pi
```sh
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
```
2. run the container
```sh
docker run --privileged -d ghcr.io/donbing/bitbot:main
```
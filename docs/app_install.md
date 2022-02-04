# Setup Options

## 🎴 A. Burn the Bitbot image to a new SD card
> Simple installation that anyone can complete
1. download the latest release from [releases page](https://github.com/donbing/bitbot/releases)  
2. use [Balena Etcher](https://www.balena.io/etcher/) to burn the zipped image to your SD card.
3. insert SD, power up and wait for the screen to refresh
## 🍓B. Add Bitbot to an existing PiOS install
> tested on buster, seems to work on bullseye too 
1. Make sure python, pip, git and other dependancies are installed
```sh
sudo apt update -y
sudo apt install -y git python3-pip python3-rpi.gpio libatlas-base-dev libopenjp2-7 libtiff5 libxcb1 libfreetype6-dev
```  
2. Clone this repo and install [pip requirements](/requirements.txt)
```sh
git clone https://github.com/donbing/bitbot
cd bitbot 
pip3 install --user -r requirements.txt
```
3. ensure that `I2C`/`SPI` are enabled on the host pi
```sh
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
```
4. Test the app 
```sh
python3 -m run
```
5. Add cron jobs to start the [app](/run.py) and [config-server](/src/config_webserver.py) after reboot
```sh
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && cd /home/pi/bitbot && python3 run.py") | crontab -
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && cd /home/pi/bitbot && python3 src/config_webserver.py") | crontab -
```
## 🐳 C. Run in docker
> 
1. ensure that `I2C`/`SPI` are enabled on the host pi
```sh
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
```
2. run the container
```sh
docker run --privileged --restart unless-stopped -d ghcr.io/donbing/bitbot:release
```

# ⚙️ Installation Options

# 🎴 **A**. Burn the Bitbot image to a new SD card
> Simple installation that anyone can complete
1. download the latest release from [releases page](https://github.com/donbing/bitbot/releases)  
2. use [Balena Etcher](https://www.balena.io/etcher/) to burn the zipped image to your SD card.
3. insert SD, power up and wait for the screen to refresh


# 🍓 **B**. Add Bitbot to an existing PiOS install
> tested on 2024 pios lite release

## 🖨️ Enable Hardware interfaces
> The inky needs i2c/spi
### Enable SPI overlay 
```sh
sudo sed -i '/dtoverlay=/d' /boot/firmware/config.txt
sudo bash -c 'echo "dtoverlay=spi0-0cs" > /boot/firmware/config.txt'
```
### Ensure that `I2C`/`SPI` are enabled on the host pi
```sh
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
```

## 💾 Install the app
> Setup Python, pull bitbot repo and install requirements

Make sure python, pip, git and other dependancies are installed
```sh
sudo apt update -y
sudo apt install -y git python3-pip python3-rpi.gpio libatlas-base-dev libopenjp2-7 libtiff5 libxcb1 libfreetype6-dev
python -m pip install --upgrade pip
```  

Clone this repo 
```sh
git clone https://github.com/donbing/bitbot
cd bitbot 
```

Start `VENV` and install [python requirements](/requirements.txt)
```sh
python -m venv venv
source venv/bin/activate
pip3 install -v --prefer-binary --extra-index-url https://www.piwheels.org/simple -r requirements.txt
```

Test the app 
```sh
python3 -m run
```

Add cron jobs to start the [app](/run.py) and [config-server](/src/configuration/config_webserver.py) after reboot
```sh
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && cd /home/pi/bitbot && python3 run.py") | crontab -
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && cd /home/pi/bitbot && python3 src/configuration/config_webserver.py") | crontab -
```

# 🐳 **C**. Run in docker
> Requires hardware interfaces to be enabled on the host

1. install docker
```sh
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

2. run the container
```sh
docker run --privileged --restart unless-stopped -d ghcr.io/donbing/bitbot:release
```

## **BitBot**, *A Raspberry Pi powered e-ink screen with crypto price chart*  
<div>
    <img height="200" src="docs/bit-bot.jpg">
    <img height="200" src="docs/bitbot-v2.png">
    <img height="200" src="docs/last_display.png">
</div>

# Basic features
 - shows the current price
 - shows instrument details (e,g, ```(XBTUSD, +12%)```)
 - displays some AI text comment/message depending on price action
 - capable of charting and trading on many different crypto-exchanges
 - reddit discussion [here](https://www.reddit.com/r/raspberry_pi/comments/mrne5p/my_eink_cryptowatcher/) 
 - warns on connection errors

# Device setup
>Burn a copy of [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/) to your micro SD  

 > install wifi connection helper, provided by https://github.com/jasbur/RaspiWiFi
```sh
git clone https://github.com/jasbur/RaspiWiFi
cd RaspiWiFi
sudo python3 initial_setup.py
```

>Install Git, pip and inky (plus some dependencies)
```sh
sudo apt-get install git python3-pip libffi-dev libjpeg62 libopenjp2-7-dev libatlas-base-dev
curl https://get.pimoroni.com/inky | bash
```  

>clone this repo add cron jobs
```sh
git clone https://github.com/donbing/bitbot
cd bitbot
pip3 install -r requirements.txt
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && python3 /home/pi/bitbot/run.py")| crontab -
(crontab -l 2>/dev/null; echo "*/10 * * * * python3 /home/pi/bitbot/run.py")| crontab -
```
   
>Run the app (or wait for cron)
```sh
python3 -m run
```

# Requested Features
 - show value of your portfolio
 - display Transaction fees
 - smaller/cheaper display
 - easier config (web app)
 - regular stocks
 - inset candles to avoid overlap of axis ticks

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
 > wifi connection script provided by https://github.com/jasbur/RaspiWiFi
```sh
git clone https://github.com/jasbur/RaspiWiFi
cd RaspiWiFi
sudo python3 initial_setup.py
```

>Install the inky libs & configure pi for the inky display
```sh
curl https://get.pimoroni.com/inky | bash
```

>Apt get python and all the other packages we need
```sh
sudo apt-get install -y python-dev libffi-dev build-essential libjpeg62 libopenjp2-7-dev libatlas-base-dev python3-pip
```

>Pip install python packages
```sh
pip3 -install requirements.txt
```

>Set the graph to auto refresh
```sh
crontab -e
```
At the end of the file, add the following commands with your correct file path and save
```sh
@reboot sleep 30 && python3 /'file'/'path'/update_chart.py
*/10 * * * * python3 /'file'/'path'/update_chart.py
```
   
>Run the app
```sh
python3 -m update_chart
```

# Requested Features
 - show value of your portfolio
 - display Transaction fees
 - smaller/cheaper display
 - easier config (web app)
 - regular stocks
 - inset candles to avoid overlap of axis ticks

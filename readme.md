# bit bot
**A Raspberry Pi powered e-ink screen with crypto price chart**

![device](bit-bot.jpg)
![screenshot](last_display.png)

 - shows the current price
 - shows instrument details (e,g, ```(XBTUSD, hi:200, lo: 2)```)
 - displays some AI text comment/message depending on input data
 - libs are capable of reading and trading on many different crypto-exchanges
 - reddit discussion [here](https://www.reddit.com/r/raspberry_pi/comments/mrne5p/my_eink_cryptowatcher/) 


# App setup
1. Install the inky libs & configure pi for the inky display
    ```sh
    curl https://get.pimoroni.com/inky | bash
    ```

2. Apt get python and all the other packages we need
    ```sh
    sudo apt-get install -y python-dev libffi-dev build-essential libjpeg62 libopenjp2-7-dev libatlas-base-dev python3-pip
    ```

3. Pip install python packages
    ```sh
    pip3 -install requirements.txt
    ```

4. Configure a bitmex api account (if you want to buy/sell)
    - Currently this is just bitmex, but ccxt supports many more
    - bitmex api key/pass must to be added to the python code in [bitmex_ccxt.py](bitmex_ccxt.py)

5. Set the graph to auto refresh
    ```sh
    crontab -e
    ```
    At the end of the file, add the following commands with your correct file path and save
    ```sh
    @reboot sleep 30 && python3 /'file'/'path'/update_chart.py
    */10 * * * * python3 /'file'/'path'/update_chart.py
    ```
   
7. Run the app
    ```sh
    python3 -m update_chart
    ```

# Device setup
 > wifi connection script provided by https://github.com/jasbur/RaspiWiFi
```sh
git clone https://github.com/jasbur/RaspiWiFi
cd RaspiWiFi
sudo python3 initial_setup.py
```

# Dumb ideas
 - alert & refresh on spikes
 - maybe an indicator light too
 - noises?
 - display max/min for today
 - buy button
 - timespan slider pot

# Todo
 - display a message if the app cannot connect to the internet
 - easily changeable exchange/instrument
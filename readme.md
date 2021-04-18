# bit bot
**A Raspberry Pi powered e-ink screen with crypto price chart**

![](candle2.png)

 - hilights the current price
 - shows instrument details (e,g, ```(XBTUSD, hi:200, lo: 2)```)
 - displays some AI text comment/message depending on input data
 - libs are capable of reading and trading on many different crypto-exchanges
 
# setup
1. Install the inky libs & configure pi for the inky display
    ```sh
    curl https://get.pimoroni.com/inky | bash
    ```
2. Enable SPI and I2C in the pi's boot config and give our user permissions
    ```sh
    sudo apt-get update
    # spi comms have to be enabled
    sudo bash -c 'echo dtparam=spi=on >> /boot/config.txt'
    sudo bash -c 'echo dtparam=i2c_arm=on >> /boot/config.txt'
    # user must be in i2c group
    sudo groupadd i2c 
    # own the /dev/i2c
    sudo chown :i2c /dev/i2c-1
    sudo chmod g+rw /dev/i2c-1
    sudo usermod -aG i2c $USER
    sudo usermod -aG kmem $USER
    ```   
3. Apt get python and all the other packages we need
    ```sh
    # this's from some heavy fuckery on the arm6 chip, probs not needed now
    sudo apt install python-dev
    sudo apt install libffi-dev
    sudo apt-get install build-essential
    sudo apt-get install libjpeg62
    sudo apt-get install libopenjp2-7-devy
    sudo apt-get install libatlas-base-dev
    ```
4. Pip install python packages
    ```sh
    sudo apt install python-numpy
    sudo pip install cffi
    sudo pip install mpl_finance
    # ccxt for crypto data, inkky for displaysudp
    sudo pip install ccxt
    sudo pip install inky
    ```
5. Configure your account
    - Currently this is just bitmex, but ccxt supports many more
    - butnex api key;pass have to be added to the python code in [bitmex_ccxt.py](bitmex_ccxt.py)
6. Run the app
    ```sh
    python -m update_chart.PY
    ```

# future plans
 - alert & refresh on spikes
 - maybe an indicator light too
 - noises?
 - display max/min for today
 - buy button
 - timespan slider pot
 




# 📈 How to configure your new crypto-watcher
1. Optionally, remove the screen protoector that is covering the e-paper display (there is a red tab at the bottom-left)
2. **Connect a micro-usb** cable to the raspberry pi board on your crypto-watcher
3. **Wait a minute** or so for it to boot up
4. The device will display a `**NO INTERNET CONNECTION**` message
5. From another device, **connect** to the `Comitup {nnn}` access point 
6. Select your internet-connected **wifi access point name**
7. Enter your **wifi password**
8. **Wait** for the device to reboot (this may take 1-2 mins)
    * Your crypto-watcher will **refresh** the screen once it has loaded up and connected to the internet.
    * The device is set up to refresh on the hour and every **ten minutes** thereafter. 
    * The current instrument defaults to **Bitmex BTC/USD**.
 
# 💻 Help
> **Source code** for the application can be found at: https://github.com/donbing/bitbot  

> For **technical assistance** please contact us via the [Etsy shop](https://www.etsy.com/uk/shop/TurtlefishDesigns), or raise a [github issue](https://github.com/donbing/bitbot/issues)

# ⚙️ Advanced Configuration
Configuration for your crypto-watcher is stored in a config.ini file on the raspberry pi  

> visit bitbot:8080 in your browser to edit the configuration file  

> SSH is enabled and can be accessed using the following command.
```sh 
ssh pi@bitbot
# password is raspberry
```
> A list of supported crypto-exchanges can be found here https://github.com/ccxt/ccxt/wiki/Exchange-Markets  

> Please see your selected exchange for the instruments that it supports

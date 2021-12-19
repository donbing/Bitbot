# How to configure your new crypto-watcher
1. **Connect a micro-usb** cable to the raspberry pi board on your crypto-watcher
2. **Wait a minute** or so for it to boot up
3. The device will display a `**NO INTERNET CONNECTION**` message
4. From another device, **connect** to the `RaspiWiFiSetup` access point 
5. **Go to `RaspPiWifiSetup.com` or `10.0.0.1`** in the browser on your device
6. Select your internet-connected **wifi access point name**
7. Enter your **wifi password**
8. **Wait** for the device to reboot (this may take 1-2 mins)
    * Your crypto-watcher will refresh the screen as soon as its loaded up and connected to the internet.
    * The device is set up to refresh on the hour and every ten minutes thereafter. 
    * The current bitcoin price defaults to **Bitmex BTC/USD**.
 
> Source code for the application can be found at: https://github.com/donbing/bitbot  
> For technical assistance please contact BingsBots via the Etsy shop.  

# Advanced Configuration
> config settings for your crypto-watcher are stored in a config-file the raspberry pi,
> in order to access the data, you will need SSH access using the following command.
```sh 
ssh pi@bitbot
# password is cryptonomicon
```
> once you have connected, the config can be opened for editing by issuing the following command
```sh
nano bitbot/config.ini
```
> the only values i reccoment altering are `exchange`, `instrument` and `comments`  
> a list of supported crypto-exchanges can be found here https://github.com/ccxt/ccxt/wiki/Exchange-Markets  
> please see your selected exchange for the instruments that it supports

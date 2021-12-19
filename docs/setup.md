# How to configure your new crypto-watcher
1. Optionally, remove the screen protoector that is covering the e-paper display (there is a red tab at the bottom-left)
2. **Connect a micro-usb** cable to the raspberry pi board on your crypto-watcher
3. **Wait a minute** or so for it to boot up
4. The device will display a `**NO INTERNET CONNECTION**` message
5. From another device, **connect** to the `RaspiWiFi Setup` access point (ignoring any warnings about it having no internet)
6. **Go to `RaspPiWifiSetup.com` or `10.0.0.1`** in the browser on your device
7. Select your internet-connected **wifi access point name**
8. Enter your **wifi password**
9. **Wait** for the device to reboot (this may take 1-2 mins)
    * Your crypto-watcher will refresh the screen once it has loaded up and connected to the internet.
    * The device is set up to refresh on the hour and every ten minutes thereafter. 
    * The current bitcoin price defaults to **Bitmex BTC/USD**.
 
> Source code for the application can be found at: https://github.com/donbing/bitbot  
> For technical assistance please contact us via the Etsy shop.  

# Advanced Configuration
> Config settings for your crypto-watcher are stored in a config-file on the raspberry pi,
> in order to access the data, you will need SSH access using the following command.
```sh 
ssh pi@bitbot
# password is raspberry
```
> Once you have connected, the config can be opened for editing by issuing the following command
```sh
nano bitbot/config.ini
```
> The only values I reccomend altering are `exchange`, `instrument` and `comments`  
> A list of supported crypto-exchanges can be found here https://github.com/ccxt/ccxt/wiki/Exchange-Markets  
> Please see your selected exchange for the instruments that it supports

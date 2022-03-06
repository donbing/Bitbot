# 📈 How to configure your new crypto-watcher
1. Optionally, remove the screen protoector that is covering the e-paper display (there is a red tab at the bottom-left)
2. **Connect a micro-usb** cable to the raspberry pi board on your crypto-watcher
3. **Wait a minute** or so for it to boot up
4. The device will display a short **intro sequence** for you to follow
5. From another device, **connect** to the `bitbot-{nnn}` access point 
6. Select your home **wifi access point name**
7. Enter your **wifi password**
8. **Wait** for the device to reboot (this may take 1-2 mins)
    * Your crypto-watcher will **refresh** the screen once it has loaded up and connected to the internet.
    * The device is set up to refresh every **ten minutes**. 
    * The dispayed instrument defaults to **Bitmex BTC/USD**.

> More detailed [instructions with screenshots can be found here](wifi_setup.md)

# ⚙️ Advanced Configuration
### Configuration for your crypto-watcher is stored in a `config.ini` file on the raspberry Pi 

 - Visit [http://bitbot:8080](http://bitbot:8080) in your browser to **edit the configuration**  
 - Edit the config file directly see [💾 **Config** Options](docs/config_options.md)
 - A list of **supported crypto-exchanges** can be found [here](https://github.com/ccxt/ccxt/wiki/Exchange-Markets)  
   - Please see your selected exchange for the ***instruments that it supports***

### Bitbot uses [Style Files](../config/base.mplstyle) to control the chart layout. 
 - If you're feeling experimental.. you can edit these! Examples of the ***styling*** options can be [found here](https://matplotlib.org/stable/tutorials/introductory/customizing.html#the-default-matplotlibrc-file)

### Inky Impression **Button** support
 - toggle_picure_frame_mode
 - refresh_display
 - toggle_volume
 - toggle_extended_view

# 💻 Help
> **Source code** for the application can be found at: https://github.com/donbing/bitbot  

> For **technical assistance** please contact us via the [Etsy shop](https://www.etsy.com/uk/shop/TurtlefishDesigns), or raise a [github issue](https://github.com/donbing/bitbot/issues)

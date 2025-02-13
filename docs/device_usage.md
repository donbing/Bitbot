# 📈 Configure your **Crypto Watcher**

## Physical setup
1. Remove the screen protector that is covering the e-paper display (there is a red tab at the bottom-left)
1. **Connect a micro-usb** cable 🔌 to the raspberry pi board on your crypto-watcher
1. **Wait a minute** ⌚ or so for it to boot up

## First tine setup
1. A short **intro sequence** 📺 may be displayed (this only happens once)
1. From another device, *connect* to the `bitbot-{nnn}` **wifi access point**
    - ⚠️ on **mobile decives**, you may need to **disable mobile data here**
1. if you are not automaticaly shown the config web page, open your browser and goto google.com. the page should then load.
    - ⚠️ if this fails please use `http://10.41.0.1` in the browser url
1. Select your **home wifi access point name** 🛜
1. Enter your **wifi password** 🙈
1. **Wait** for the device to reboot ♻️ (this may take 1-2 mins)
    * you many need to go **back to #5, or restart** the device if there's no action within **5 minutes** 
    * Your crypto-watcher will **refresh** the screen once it has **loaded up and connected** to the internet.
    * The device is set up to **refresh** every **thirty minutes**. 
    * The dispayed instrument defaults to **Coinbase BTC/USD**.

> More detailed [instructions with screenshots can be found here](wifi_setup.md)

# ⚙️ Advanced Configuration
### Visit [http://bitbot:8080](http://bitbot:8080) in your browser to **edit the configuration**  

 - Configuration for your crypto-watcher is stored in a `config.ini` file on the raspberry Pi 
 - Edit the config file directly see [💾 **Config** Options](docs/config_options.md)
 - A list of **supported crypto-exchanges** can be found [here](https://github.com/ccxt/ccxt/wiki/Exchange-Markets)  
   - Please see your selected exchange for the ***instruments that it supports***

### Bitbot uses **matplotlib [Style Files](../config/mpl_styles/base.mplstyle)** to control the chart layout. 
 - edit these if you're feeling experimental, Examples of the ***styling*** options can be [found here](https://matplotlib.org/stable/tutorials/introductory/customizing.html#the-default-matplotlibrc-file)

### Inky Impression **Button** support 
 - toggle_picure_frame_mode
 - refresh_display
 - toggle_volume
 - toggle_extended_view

# 💻 Help
> **Source code** for the application can be found at: https://github.com/donbing/bitbot  

> For **technical assistance** please contact us via the [Etsy shop](https://www.etsy.com/uk/shop/TurtlefishDesigns), or raise a [github issue](https://github.com/donbing/bitbot/issues)

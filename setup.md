# How to configure your new crypto-watcher
1.	Connect the SD card to your PC
    *	Remove the SD card from the Pi
    *	Insert the SD card into the reader (supplied)
    *	DO NOT format the drive (even if Windows asks you to)
2.	Save your wi-fi details onto the SD card
    *	Open notepad on your PC
    *	Enter the following text:
    ```
    country=us
    update_config=1
    ctrl_interface=/var/run/wpa_supplicant

    network={
    scan_ssid=1
    ssid="MyNetworkSSID"
    psk="Pa55w0rd1234"
    }
3. Configure your personal wifi login info
    *	Change '**country**' to your two letter ISO country code
    *	Change '**ssid**' to your wifi network name
    *	Change '**psk**' to your wifi password
    * 	Save the notepad file as **‘wpa_supplicant.conf’** on the boot drive of the SD card
    * More information about configuring your Pi’s wifi can be found here: https://www.raspberrypi-spy.co.uk/2017/04/manually-setting-up-pi-wifi-using-wpa_supplicant-conf/
 
3.	Power up your Pi and wait
    * Put the SD card back in your Pi and power on the Pi by connecting the micro USB cable to the Pi and a power source.
    * Your crypto-watcher will refresh the screen as soon as its loaded up and connected to the internet.
    * The device is set up to refresh on the hour and every ten minutes thereafter. 
    * the current bitcoin price is taken in USD from Bitmex.
 
 - Source code for the application can be found at: https://github.com/donbing/bitbot
 - For technical assistance please contact BingsBots via the Etsy shop.
 
 

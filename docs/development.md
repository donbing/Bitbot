# App Development

> Bitbot is somewhat cobbled together, but is fairly carefully commented and has been factored with ease of change in mind.  

# Tests
> How to run.
```sh
python3 -m unittest discover tests -v
```


## logging
BitBot will log to `StdOut` and a rolling `debug.log` file, i'm mildly concerned about writing to the SD card too much causing wear, it may be sensible to write these to a memory cache instead.

Log level is defaulted to info, but there is some limited debug level logging if you wish to get more info.

Cron jobs were configured to output to syslog.

```sh
# python logging
tail ~/bitbot/debug.log
# syslog logging
more /var/log/syslog | grep bitbot.charts
```

## Packages
 - Pimoroni's [`inky`](https://github.com/pimoroni/inky) lib is used to draw to the screen, 
 - [`CCXT`](https://github.com/ccxt/ccxt) is used to interact with currency exchanges
 - [`MPL-Finance`](https://github.com/matplotlib/mpl-finance) is used to draw the graphs (and could do with updating to [`mplfinance`](https://github.com/matplotlib/mplfinance))
 - [`Pillow`](https://github.com/python-pillow/Pillow) aids in drawing overlay text onto the graph

![Package Interactions](http://www.plantuml.com/plantuml/svg/3Oon3KCX30NxFqMo0EvJ_LN0M7mhO11-LjOFrUckkDkHDsBqwwt6FQh4xgy7MFuXslcNckA94YwRfq4CYUUWEgseDIgACa4Zgvt6JcT5A_CtD_6qZbstM3ty0m00)

## Docker
> Build arm6 on x86
```bash
docker buildx build --platform linux/armv6 . -t bitbot --progress string
# run it
docker run --privileged --platform linux/arm/v6 bitbot
```

## Configuration
[`RaspiWifi`](https://github.com/jasbur/RaspiWiFi) is installed seperately in order to facilitate easy end-user setup. Unfortunately  the lack of region in wpa_supplicant causes problems on newer pi hardware. they could do with a PR to fix..  

Alternativey [`txwifi`](https://github.com/txn2/txwifi) may be worth a look as a replacement, and is hosted in docker for cleanliness and consistency. 
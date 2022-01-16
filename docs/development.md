# Development

> Bitbot is somewhat cobbled together, but is fairly carefully commented and has been factored with ease of change in mind.  

## ✔️ Tests 
> [python unittests](/tests) with the default test framework 
    
    python3 -m unittest discover tests -v

## ✉️ Env vars 
> env vars `TESTRUN` loads one chart and exits, `BITBOT_SHOWIMAGE` [opens the image in vscode](/run.py)

    export TESTRUN=true BITBOT_OUTPUT=disk BITBOT_SHOWIMAGE=true

## 🌳logging 
> BitBot will log to `StdOut` and a rolling `debug.log` file, configured in [📁logging.ini](/logging.ini)

> Log level is **defaulted to `INFO`**, but there is some ***limited debug level logging*** if you wish to get more info.

> Cron jobs were configured to output to syslog. 😞, python should do this
```sh
# python logging
tail ~/bitbot/debug.log
# syslog logging
less /var/log/syslog | grep bitbot.charts
```

## 🎁 Packages 
 - [Pimoroni](pimoroni.com) [`inky`](https://github.com/pimoroni/inky) does the **e-ink display**, 
 - [`CCXT`](https://github.com/ccxt/ccxt) talks to **crypto exchanges**
 - [`MPL-Finance`](https://github.com/matplotlib/mpl-finance) **draws the graphs** (and could do with updating to [`mplfinance`](https://github.com/matplotlib/mplfinance))
 - [`Pillow`](https://github.com/python-pillow/Pillow) draws **drawing overlay** text onto the graph

![Package Interactions](http://www.plantuml.com/plantuml/svg/3Oon3KCX30NxFqMo0EvJ_LN0M7mhO11-LjOFrUckkDkHDsBqwwt6FQh4xgy7MFuXslcNckA94YwRfq4CYUUWEgseDIgACa4Zgvt6JcT5A_CtD_6qZbstM3ty0m00)

## 🐳 Docker 
> **Github actions** builds and tests and publishes a **container image** on each commit to `main` and `release`
### 🐳 Build 
> building on `x86` is way faster than on the Pi  
```sh
# remove the `--platform` args if building on a pi
docker buildx build --platform linux/armv6  . -t bitbot -f scripts/docker/dockerfile --progress string
```
### 🐳 Run
> **Priviledged access** is needed for `GPIO`, this looks to be fixable thru bind mounts  
```sh
    docker run --privileged --platform linux/arm/v6 bitbot
```
## 📻 Easy WiFi config 
[`comitup`](https://github.com/davesteele/comitup) is used for the ***disk image***, it creates a **config hotspot** on the Pi if it **cant connect** to any wifi itself.
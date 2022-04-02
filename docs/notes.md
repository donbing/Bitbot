todo:
 - ## layout 
   * fit candle count to screen size
   - keep an eye on the overlay least intrusive position algo, seems to be flaky

 - ## multi-currency support
   - button to toggle between curencies
   - multi-plot display 
   - overlapping coloured multi-coin charts
   
 - ## impression:
    - better button actions!
     - make these state-based, so photo mode behaves different to chart mode
    - larger intro font
    - larger label fonts
    - config candle colours
    - config volume colours

 - ## config server
    - use friendly config forms
    - allow selecting style in config

 - ## general
    - on-screen assembly instructions
    - moving averages
    - indicators


> Build arm6 on x86
```bash
 docker run -e QEMU_CPU=arm1176 --privileged --rm -it --platform linux/arm/v6 balenalib/raspberry-pi:buster bash
# build container atrm6
docker buildx build --platform linux/arm/v6 . -t bitbot --progress string
# run it, have to specify which chip QEMU should emulate
docker run -e QEMU_CPU=arm1176 --privileged --rm -t --platform linux/arm/v6 navikey/raspbian-buster:latest bash

docker buildx build --platform linux/arm/v6 . -t bitbot -f scripts/docker/dockerfile --progress string
docker run -e QEMU_CPU=arm1176 --privileged --rm -it --platform linux/arm/v6 bitbot

# remove all containers
docker container rm $(docker container ls -q -a)
#' which cpus to use for the build 
--cpuset-cpus=0-3'
# wifi-connect docker pull balenablocks/wifi-connect:rpi
docker run --network=host -v /run/dbus/:/run/dbus/ balenablocks/wifi-connect:rpi

# error: failed to solve: failed to solve with frontend dockerfile.v0: failed to create LLB definition: rpc error: code = Unknown desc = error getting credentials - err: exit status 255, out: ``
= In ~/.docker/config.json `change credsStore to credStore`

# error exec "--env" "executable file not found in $PATH: unknown"
= badly ordered docker args, envs must come before image name

# test run 
docker run --rm --env BITBOT_TESTRUN=true --env BITBOT_OUTPUT=disk --env BITBOT_SHOWIMAGE=false  bb
```

> get linux os version
```sh
cat /etc/os-release
```

> enable vnc raspiconfig
```sh
sudo raspi-config nonint do_vnc 0
```

> setup my git
```sh
# setup user
git config --global user.email ccbing@gmail.com
git config --global user.name donbing
# tell git to cache creds after first auth
git config --global credential.helper store
# remove creds
git config --global --unset user.password
# aliases
 git config --global alias.co checkout
 git config --global alias.br branch
 git config --global alias.ci commit
 git config --global alias.st status
```
> check cpu arch 
```sh
dpkg --print-architecture
```


## fonts
> place in `~/.fonts` or `/usr/local/share/fonts` for system wide access
    mkdir ~/.fonts && cp ~/bitbot/src/resources/04B_03__.TTF ~/.fonts/04B_03__.TTF

> manually rebuild the font cache with `fc-cache -f -v`

> list fonts with `fc-list`



# balena
```
# install gbalena cli
wget https://github.com/balena-io/balena-cli/releases/download/v13.3.0/balena-cli-v13.3.0-linux-x64-standalone.zip
unzip balena-cli-v13.3.0-linux-x64-standalone.zip
# balena cli
balena login
balena push gh_donbing/teste
# git
# add pud key to balena
balena key add Main ~/.ssh/id_rsa.pub
# list keys
balena keys
# push to balena
git remote add balena gh_donbing@git.balena-cloud.com:gh_donbing/teste.git
# push our main branch to balena master branch
git push balena main:master
```


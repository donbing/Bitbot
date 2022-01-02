# Docker setup instructions

1. update the host package manager
```sh
sudo apt-get update && sudo apt-get upgrade
```
2. install docker & reboot
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
3. setup user
```sh
sudo usermod -aG docker pi
```
4. Reboot
```sh
sudo shutdown -r now
```
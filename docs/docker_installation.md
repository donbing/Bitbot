# 🐋 How to install Docker

1. ### Update the host package manager
```sh
sudo apt update -y 
```
2. ### Install docker
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
3. ### Setup user
```sh
sudo usermod -aG docker pi
```
4. ### docker compose
```sh
sudo curl -fL 'https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-armv6' -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
5. ### Reboot
```sh
sudo shutdown -r now
```
6. ### Run bitbot image

 - `main`
    ```shell
    docker run --restart unless-stopped --privileged ghcr.io/donbing/bitbot:main
    docker run -it --privileged ghcr.io/donbing/bitbot:main
    docker-compose -f scripts/docker/docker-compose.yml up
    ```
 - `release` (stable)
    ```shell
    docker run --restart unless-stopped --privileged ghcr.io/donbing/bitbot:release
    ```
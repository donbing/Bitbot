# Docker setup instructions

1. ### Update the host package manager
```sh
sudo apt-get update && sudo apt-get upgrade
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
4. ### Reboot
```sh
sudo shutdown -r now
```
5. ### Run bitbot image

 - `main`
    ```shell
    docker run --privileged ghcr.io/donbing/bitbot:main
    ```
 - `release` (stable)
    ```shell
    docker run --privileged ghcr.io/donbing/bitbot:release
    ```
 - `keep running`
    ```shell
    docker run --restart unless-stopped --privileged ghcr.io/donbing/bitbot:release
    ```
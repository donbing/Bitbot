FROM python:3.9.9-bullseye

# install required packages
RUN apt-get update -y 
RUN apt-get install -y rustc rpi.gpio gcc python3-dev python3-rpi.gpio

# set the working directory in the container
WORKDIR /code

# copy the content of the local src directory to the working directory
COPY . .

# install dependencies
RUN pip3 install -U pip
ARG CFLAGS=-fcommon 
RUN pip3 install -r requirements.txt

# command to run on container start
CMD [ "python3", "./run.py" ]

#sudo docker build . -t bitbot
#docker run -privileged --device /dev/gpiomem -d bitbot

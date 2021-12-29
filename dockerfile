FROM python:3.9.9-bullseye

# install required packages
RUN apt-get update -y && apt-get install -y rustc gcc python3-pip python3-dev
# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

#RUN apt-get install -y python3-dev python3-rpi.gpio
ARG CFLAGS=-fcommon 
RUN pip3 install rpi.gpio

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python3", "./run.py" ]

#sudo docker build . -t bitbot
#docker run --device /dev/gpiomem -d bitbot

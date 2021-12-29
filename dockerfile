FROM python:3.9.9-bullseye

# install required packages
RUN apt-get update -y && apt-get install -y rustc gcc

# set the working directory in the container
WORKDIR /code

# copy the content of the local src directory to the working directory
COPY . .

# install dependencies
ARG CFLAGS=-fcommon 
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

# command to run on container start
CMD [ "python3", "./run.py" ]
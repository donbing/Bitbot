FROM python:3.9.9-slim-bullseye AS compile-image

# install required packages
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    g++ \
    rustc \
    gcc \
    cargo \
    libffi-dev \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev

# set the working directory in the container
WORKDIR /code

# install dependencies
ARG CFLAGS=-fcommon 
RUN pip3 install -U pip

COPY requirements.txt .
RUN pip3 install --user --no-cache-dir -r requirements.txt

# create app image
FROM python:3.9.9-slim-bullseye AS build-image
COPY --from=compile-image /root/.local /root/.local

# packages needed to run the app
RUN apt-get update && apt-get install -y \
    libfreetype6 \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# copy the content of the local src directory to the working directory
COPY . .

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH
# command to run on container start
CMD [ "python3", "./run.py" ]
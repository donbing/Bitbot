FROM python:3.9.9-bullseye AS compile-image

# install required packages
RUN apt-get update -y && apt-get install -y --no-install-recommends rustc gcc cargo

# set the working directory in the container
WORKDIR /tmp

# install dependencies
# ARG CFLAGS=-fcommon 
RUN pip3 install -U pip

COPY requirements.txt .
RUN pip3 install --user --no-cache-dir --index-url=https://www.piwheels.org/simple/ -r requirements.txt

# create app image
FROM python:3.9.9-slim-bullseye AS build-image
COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /code
# packages needed to run the app
RUN apt-get update && apt-get install -y \
    libfreetype6 \
    libopenjp2-7-dev \
    libjpeg62 \
    libtiff5 \
    libatlas-base-dev \
    libxcb-xinput0 \
    && rm -rf /var/lib/apt/lists/*

# copy the content of the local src directory to the working directory
COPY . .

# Make sure scripts in .local are usable:
# command to run on container start
CMD [ "python3", "./run.py" ]
FROM python:3.9.9-bullseye AS compile-image

# install required packages
RUN apt-get update -y && apt-get install -y --no-install-recommends rustc gcc cargo

# install dependencies
ARG CFLAGS=-fcommon 
RUN pip3 install -U pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir --user -r requirements.txt

FROM python:3.9.9-bullseye AS build-image
COPY --from=compile-image /root/.local /root/.local

# set the working directory in the container
WORKDIR /code
# copy the content of the local src directory to the working directory
COPY . .

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH
# command to run on container start
CMD [ "python3", "./run.py" ]
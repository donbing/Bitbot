FROM debian:bullseye-slim AS base-image
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y \
    --no-install-recommends \
    python3 python3-rpi.gpio libatlas-base-dev libopenjp2-7 libtiff5 libxcb1 libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/* 

FROM base-image AS build-image
RUN apt update -y
RUN apt install -y git gcc python3-pip 
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -v --prefer-binary --extra-index-url https://www.piwheels.org/simple --user -r requirements.txt 

FROM base-image AS release-image
COPY --from=build-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
WORKDIR /code
COPY . .
CMD [ "python3", "./run.py" ] 
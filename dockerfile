FROM navikey/raspbian-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6 \
    libopenjp2-7-dev \
    python3 python3-pip \
    libtiff5 \
    libatlas-base-dev \
    libxcb-xinput0 \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY . .

CMD [ "python3", "./run.py" ]
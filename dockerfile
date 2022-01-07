FROM navikey/raspbian-buster 
#balenalib/raspberry-pi-buster::latest
ENV QEMU_CPU=arm1176
ENV CFLAGS=" -marm -mfpu=vfp -mtune=arm1176jzf-s -mfloat-abi=softfp"
RUN apt-get update && apt-get install -y --no-install-recommends\
    python3 python3-pip \
    python3-matplotlib \
    python3-rpi.gpio \
    python3-pil \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY . .

CMD [ "python3", "./run.py" ]
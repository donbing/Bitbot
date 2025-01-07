FROM python:3.11-slim-bookworm

# avoid bytecode baggage
ENV PYTHONDONTWRITEBYTECODE=1

# venv to keep python happy
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# update pip
RUN python3 -m pip install --upgrade pip --no-cache-dir

# install python reqs
COPY requirements.txt .
RUN python3 -m pip install -v \
    --prefer-binary \
    --no-cache-dir \
    -r requirements.txt \
    --extra-index-url https://www.piwheels.org/simple 

# install OS reqs
RUN apt-get update -y && \
    apt-get install -y \
    --no-install-recommends \
    libopenblas-dev libopenjp2-7 libtiff6 libxcb1 libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/* 

# prep app code
WORKDIR /code
COPY . .
CMD ["python", "run.py"]
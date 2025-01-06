
FROM debian:bookworm-slim AS base-image
RUN apt-get update -y && apt install -y \
    --no-install-recommends \
    python3  \
    && rm -rf /var/lib/apt/lists/* 

FROM base-image AS build-image
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -y && apt-get install -y python3-venv gcc python3-pip libatlas-base-dev libopenjp2-7 libtiff6 libxcb1 libfreetype6-dev 
RUN python3 -m pip install --upgrade pip --break-system-packages --no-compile --no-cache-dir

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY requirements.txt .
RUN pip install -v \
    --prefer-binary \
    --no-compile \
    --no-cache-dir \
    --extra-index-url https://www.piwheels.org/simple \
    -r requirements.txt 

FROM base-image AS release-image
COPY --from=build-image /venv /venv
ENV PATH=/venv/bin:$PATH
WORKDIR /code
COPY . .
CMD [ "python3", "run.py" ] 
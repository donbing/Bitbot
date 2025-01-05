FROM debian:bookworm-slim AS base-image
RUN apt-get update -y && apt install -y \
    --no-install-recommends \
    python3  \
    && rm -rf /var/lib/apt/lists/* 

FROM base-image AS build-image
RUN apt-get update -y
RUN apt-get install -y python3-venv gcc python3-pip
RUN pip3 install --upgrade pip --break-system-packages

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY requirements.txt .
RUN pip3 install -v \
    --prefer-binary \
    --break-system-packages \
    --extra-index-url https://www.piwheels.org/simple \
    -r requirements.txt 

FROM base-image AS release-image
COPY --from=build-image /venv /venv
ENV PATH=/venv/bin:$PATH
WORKDIR /code
COPY . .
CMD [ "python3", "./run.py" ] 
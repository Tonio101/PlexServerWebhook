FROM python:3.9.2

RUN mkdir -p /usr/src/app
COPY ./src /usr/src/app
COPY requirements.txt /usr/src/app
WORKDIR /usr/src/app

# RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "plexy_webhook.py", "--config", "plex_webhook_config.local.yml"]

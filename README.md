# Plex Server Simple Webhook

Send a text notification from a Plex Server Webhook event.

### Enable Gmail API
Follow Gmail API for developers guide on enabling the

Follow the [Gmail API documentation](https://developers.google.com/gmail/api) to enable<br>
the API for your account.

### Configure Docker

Follow the [Install Docker Engine](https://docs.docker.com/engine/install) documentation.

### Start Plex Webhook Container

Build the docker image:
```bash
./build_docker_image.sh
```
Start container:
```bash
./start_docker_container.sh
```
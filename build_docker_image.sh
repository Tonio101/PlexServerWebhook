#!/bin/bash

IMAGE_TAG="plexy:plexy_latest"
DOCKER_FILE=$(/bin/pwd)/Dockerfile

#echo -e "${IMAGE_TAG}\n${DOCKER_FILE}\n"

docker build --tag ${IMAGE_TAG} .

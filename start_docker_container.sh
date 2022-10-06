#!/bin/bash

IMAGE_TAG="plexy:plexy_latest"
IMAGE_ID=$(docker images -q $IMAGE_TAG)

#echo -e "${IMAGE_ID}"
docker run -d --network=host --restart=on-failure:5 ${IMAGE_ID}

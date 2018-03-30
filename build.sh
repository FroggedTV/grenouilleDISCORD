#!/bin/bash

REGISTRY="kuajstry.ddns.net:5000"
IMAGE_NAME="caline"
IMAGE_VERSION="1"
TOKEN="$(cat token.txt)"
API_KEY="$(cat api_key.txt)"

docker build -t $REGISTRY/$IMAGE_NAME:$IMAGE_VERSION .
docker push $REGISTRY/$IMAGE_NAME:$IMAGE_VERSION

#docker rm -f caline

#docker run -d --restart always --name caline $REGISTRY/$IMAGE_NAME:$IMAGE_VERSION $TOKEN $API_KEY

#docker logs -f caline


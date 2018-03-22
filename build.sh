#!/bin/bash

IMAGE_NAME="grenouille-discord"
IMAGE_VERSION="1"
TOKEN="$(cat token.txt)"
API_KEY="$(cat api_key.txt)"

docker build -t $IMAGE_NAME:$IMAGE_VERSION .

docker rm -f caline

docker run -d --restart always --name caline $IMAGE_NAME:$IMAGE_VERSION $TOKEN $API_KEY

docker logs -f caline

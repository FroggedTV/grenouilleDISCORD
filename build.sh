#!/bin/bash

IMAGE_NAME="grenouille-discord"
IMAGE_VERSION="1"
TOKEN="$(cat token.txt)"
API_KEY="$(cat api_key.txt)"

docker build -t $IMAGE_NAME:$IMAGE_VERSION .


sudo mkdir -p /usr/share/discord-data
docker run -it --rm -e "http_proxy=http://p-goodway:3128/" -e "https_proxy=http://p-goodway:3128/" $IMAGE_NAME:$IMAGE_VERSION $TOKEN $API_KEY

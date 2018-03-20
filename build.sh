#!/bin/bash

REGISTRY="kuajstry.ddns.net:5000/"
IMAGE_NAME="grenouille-discord"
IMAGE="$REGISTRY$IMAGE_NAME"
TOKEN="$(cat token.txt)"

docker build -t $IMAGE .
#docker push $IMAGE

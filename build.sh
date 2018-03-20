#!/bin/bash

IMAGE_NAME="grenouille-discord"
IMAGE_VERSION="1"
TOKEN="$(cat token.txt)"

docker build -t $IMAGE:$IMAGE_VERSION .

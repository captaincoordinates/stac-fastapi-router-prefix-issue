#!/bin/bash

pushd $(dirname $0)/..

pip install -r ./stac-fastapi/requirements.txt
docker-compose build

#!/usr/bin/env bash

docker build --no-cache -t complete_component:latest -f dockerfiles/Dockerfile .

docker cp DistributedNeuralSystem #nomedocker:/home/
#command that should be ex on the host
export PYTHONPATH=/home/
pip install thrift
pip install pandas



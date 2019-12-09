FROM  tensorflow/tensorflow:2.0.0-py3

MAINTAINER Giacomo Bossi "10457823@polimi.it"

COPY . /home/

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y lshw lsb-core \
    && cd home \
    && pip install -r requirements.txt


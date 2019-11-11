FROM  tensorflow/tensorflow:2.0.0-py3

MAINTAINER Giacomo Bossi "10457823@polimi.it"

RUN apt-get update && apt-get -y upgrade
RUN buildDependencies=" automake \
                        bison \
                        flex \
                        g++ \
                        git \
                        libboost-all-dev \
                        libevent-dev \
                        libssl-dev \
                        libtool \
                        make \
                        pkg-config \
                        wget \
                        "; \
                        apt-get install -y --no-install-recommends $buildDependencies lshw lsb-core && \
                        rm -rf /var/lib/apt/lists/*

RUN cd home \
    && wget http://apache.panu.it/thrift/0.13.0/thrift-0.13.0.tar.gz \
    && tar xvfz thrift-0.13.0.tar.gz \
    && cd thrift-0.13.0 \
    && ./bootstrap.sh \
    && ./configure \
    && make install \
    && cd .. \
    && rm thrift-0.13.0.tar.gz \
    && apt-get purge -y --auto-remove $buildDependencies \
	&& rm -rf /var/cache/apt/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /tmp/* \
    && rm -rf /var/tmp/*

WORKDIR /




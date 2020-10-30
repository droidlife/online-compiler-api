FROM ubuntu:trusty

RUN apt-get update

# Install Python
RUN apt-get install -y python
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN apt-get install -y python-virtualenv
RUN rm -rf /var/lib/apt/lists/*

RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install software-properties-common

# Define working directory.
WORKDIR /data

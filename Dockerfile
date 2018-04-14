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

#grab oracle java (auto accept licence)
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get install -y oracle-java8-installer

# Define working directory.
WORKDIR /data

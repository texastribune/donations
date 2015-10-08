FROM ubuntu:14.04
MAINTAINER @x110dc

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update -qq
RUN apt-get install -yq language-pack-en-base && \
  dpkg-reconfigure locales
RUN apt-get install -yq python3-pip
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

EXPOSE 80
COPY . /flask
ENTRYPOINT /bin/bash

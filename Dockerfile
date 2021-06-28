FROM python:3.9.5

# This Dockerfile is intended for development. See Dockerfile.sample for something more
# suitable for production.

ENV NODE_VERSION=node_12.x
ENV FLASK_DEBUG 1
ENV NPM_CONFIG_LOGLEVEL warn

# install Node and NPM
RUN apt-get -yq update && \
    apt-get -yq install apt-transport-https && \
    curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo "deb https://deb.nodesource.com/$NODE_VERSION stretch main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get -yq update && \
    apt-get -y install nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG ENABLE_SENTRY_RELEASE=False

COPY static /app/static
COPY webpack /app/webpack
COPY config /app/config
COPY package.json /app/
COPY package-lock.json /app/
COPY babel.config.js /app/
RUN npm install

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY dev-requirements.txt /app/
RUN pip install -r /app/dev-requirements.txt

COPY . /app

ENTRYPOINT /bin/bash

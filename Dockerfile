FROM nikolaik/python-nodejs:python3.9-nodejs12

# This Dockerfile is intended for development. See Dockerfile.sample for something more
# suitable for production.

ENV FLASK_DEBUG 1
ENV NPM_CONFIG_LOGLEVEL warn

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

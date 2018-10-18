FROM python:3.6

# This Dockerfile is intended for development. See Dockerfile.sample for something more
# suitable for production.

ENV NODE_VERSION=node_8.x
ENV FLASK_DEBUG 1
ENV NPM_CONFIG_LOGLEVEL warn

# install Node and Yarn
RUN apt-get -yq update && \
    apt-get -yq install apt-transport-https && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
    curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo "deb https://deb.nodesource.com/$NODE_VERSION stretch main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get -yq update && \
    apt-get -y install nodejs yarn

WORKDIR /app

COPY static /app/static
COPY webpack /app/webpack
COPY package.json /app/
COPY yarn.lock /app/
COPY .babelrc /app/
RUN yarn

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt
COPY dev-requirements.txt /app/
RUN pip3 install -r /app/dev-requirements.txt

COPY . /app

ENTRYPOINT /bin/bash

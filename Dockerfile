FROM node:8 as node_base

WORKDIR /app

ENV NPM_CONFIG_LOGLEVEL warn

COPY static /app/static
COPY webpack /app/webpack
COPY package.json /app/
COPY yarn.lock /app/
COPY .babelrc /app/
RUN yarn

FROM python:3.6

WORKDIR /app

COPY --from=node_base /app /app

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY . /app/
EXPOSE 80
ENTRYPOINT /bin/bash

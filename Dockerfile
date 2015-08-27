FROM x110dc/dev
MAINTAINER @x110dc

RUN apt-get install -yq language-pack-en-base && \
  dpkg-reconfigure locales
RUN pip install -U pip
RUN pip install stripe flask uwsgi

EXPOSE 80
COPY . /flask
ENTRYPOINT /bin/bash

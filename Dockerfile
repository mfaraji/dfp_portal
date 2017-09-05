FROM python:2.7

ENV PYTHONUNBUFFERED 1

# install system packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils


RUN apt-get update && apt-get install -y \
    git \
    libmysqlclient-dev \
    python-dev \
    python-pip \
    nginx \
    python-mysqldb \
    python-setuptools \
    supervisor \
    vim \
    npm \
    nodejs-legacy \
    memcached


RUN mkdir /code/
WORKDIR /code/
ADD . /code/
RUN pip install -r requirements/production.txt

COPY ./config/nginx-app.conf /etc/nginx/sites-available/default
COPY ./config/supervisor-app.conf /etc/supervisor/conf.d/

EXPOSE 8000
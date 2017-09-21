FROM ubuntu:16.04

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
    memcached

RUN mkdir /code/
WORKDIR /code/
COPY ./requirements/base.txt .
COPY ./requirements/production.txt .

RUN pip install -r production.txt

ADD . /code/


RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./config/nginx-app.conf /etc/nginx/sites-available/default
COPY ./config/supervisor-app.conf /etc/supervisor/conf.d/

RUN service supervisor start
RUN supervisorctl start inspire

EXPOSE 8000

CMD ["supervisord", "-n"]
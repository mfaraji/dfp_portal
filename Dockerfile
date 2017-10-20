FROM ubuntu:16.04
MAINTAINER Moe Faraji <faraji66@gmail.com>

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
    memcached \
    locales


RUN locale-gen en_US.UTF-8 && dpkg-reconfigure locales
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

RUN mkdir /code/
WORKDIR /code/
ADD requirements/base.txt .
ADD requirements/production.txt .
RUN pip install -r production.txt
ADD . /code/

ENV TERM dumb

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./config/nginx-app.conf /etc/nginx/sites-available/default
COPY ./config/supervisor-app.conf /etc/supervisor/conf.d/

#RUN service supervisor start
#RUN supervisorctl start inspire

EXPOSE 8000

CMD ["/usr/bin/supervisord","-n", "-c", "/etc/supervisor/supervisord.conf"]
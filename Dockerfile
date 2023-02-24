FROM almalinux:latest

WORKDIR /home/www/app

ENV LANG en_US.UTF-8
### Install dependencies
RUN yum install python39 python3-devel -y \
    && yum -y install python3-pip \
    && yum -y install rsync

COPY requirements.txt /home/www/app/
RUN /bin/bash -c "pip3.9 install --upgrade pip"
RUN /bin/bash -c "pip3.9 install -r /home/www/app/requirements.txt"

ADD . /home/www/app/
FROM debian:8

RUN apt-get update -y && \
    apt-get install software-properties-common -y

RUN apt-add-repository 'deb http://repos.ideascube.org/debian/ jessie/'

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install python3-pip libssl-dev libffi-dev software-properties-common -y && \
    apt-get install ideascube -y --force-yes

RUN pip3 install --upgrade setuptools
RUN pip3 install ansible==2.5.0
RUN mkdir -p /etc/ansible/facts.d

ENV IDEASCUBE_ID=kb
ENV DOMAIN=koombook.lan

ARG PROJECT_NAME=idb-bsf-vagrant
ENV PROJECT_NAME="${PROJECT_NAME}"

RUN ideascube collectstatic
RUN ideascube migrate --run-syncdb

COPY start_nginx_ideascube.sh /


ENTRYPOINT ./start_nginx_ideascube.sh

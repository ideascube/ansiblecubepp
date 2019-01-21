FROM debian:8
ARG ideascube_version

RUN apt-get update -y && \
    apt-get install software-properties-common -y

RUN apt-add-repository 'deb http://repos.ideascube.org/debian/ jessie/'

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install python-pip python-dev libssl-dev libffi-dev software-properties-common git -y && \
    apt-get install ideascube -y --force-yes

RUN pip install --upgrade setuptools
RUN pip install ansible==2.5.0
RUN mkdir -p /etc/ansible/facts.d

# Backup ideascube content
RUN mv /var/ideascube /var_ideascube

# Set default project name, overwrite in case env var is passed at runtime
ARG PROJECT_NAME=idb-bsf-vagrant
ENV PROJECT_NAME="${PROJECT_NAME}"

ADD http://filer.bsf-intranet.org/kiwix-serve-AMD64.v2.0 /usr/local/bin/kiwix-serve
RUN chmod 755 /usr/local/bin/kiwix-serve

COPY start_nginx_ideascube.sh /
EXPOSE 80

ENTRYPOINT ./start_nginx_ideascube.sh

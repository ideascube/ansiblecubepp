FROM debian:8
ARG ideascube_version

RUN apt-get update -y && \
    apt-get install software-properties-common -y

RUN apt-add-repository 'deb http://repos.ideascube.org/debian/ jessie/'

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install python-pip python3-pip python-dev libssl-dev libffi-dev software-properties-common git -y && \
    apt-get install ideascube -y --force-yes

RUN pip install --upgrade setuptools
RUN pip install ansible==2.5.0
RUN mkdir -p /etc/ansible/facts.d

# Clean up
RUN apt-get clean -y; \
    rm -fr \
      /usr/share/doc/* \
      /var/cache/debconf/*

# Backup ideascube content
RUN mv /var/ideascube /var_ideascube

# Set default project name, docker domain name, process_id and environment. Overwrite in case env var is passed at runtime
ARG PROJECT_NAME=idb-bsf-vagrant
ENV PROJECT_NAME="${PROJECT_NAME}"

ARG DOCKER_DOMAIN=docker.ideas-box.eu
ENV DOCKER_DOMAIN="{DOCKER_DOMAIN}"

ARG PROCESS_ID=azerty
ENV PROCESS_ID="${PROCESS_ID}"

ARG ENVIRON=PROD
ENV ENVIRON="${ENVIRON}"

ARG DEPLOYABLE=true
ENV DEPLOYABLE="${DEPLOYABLE}"

ARG PROJECT_ID=1
ENV PROJECT_ID="${PROJECT_ID}"

ARG BRANCH=master
ENV BRANCH="${BRANCH}"

ADD http://filer.bsf-intranet.org/kiwix-serve-AMD64.v2.0 /usr/local/bin/kiwix-serve
RUN chmod 755 /usr/local/bin/kiwix-serve

COPY start_nginx_ideascube.sh /
EXPOSE 80

ENTRYPOINT ./start_nginx_ideascube.sh

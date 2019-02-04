#!/bin/bash
export IDEASCUBE_ID=idb
export DOMAIN="$PROJECT_NAME.$PROCESS_ID.ideascube.$DOCKER_DOMAIN"
export KOLIBRI_DOMAIN="$PROJECT_NAME.$PROCESS_ID.ideascube"

mv /var_ideascube/* /var/ideascube/

echo "DOMAIN=$FULLDOMAIN" >> /etc/default/ideascube

ideascube migrate --run-syncdb

/usr/local/bin/ansible-pull -d /var/lib/ansible/local -i hosts -U https://github.com/ideascube/ansiblecubepp.git main.yml --extra-vars "generic_project_name=$PROJECT_NAME full_domain_name=$DOMAIN env=$ENVIRON kolibri_domain=$KOLIBRI_DOMAIN"

ideascube runserver 8000


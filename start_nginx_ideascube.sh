#!/bin/bash
export IDEASCUBE_ID=idb
export FULLDOMAIN="$PROCESS_ID.ideascube.$DOCKER_DOMAIN"

mv /var_ideascube/* /var/ideascube/

ideascube migrate --run-syncdb

/usr/local/bin/ansible-pull -d /var/lib/ansible/local -i hosts -U https://github.com/ideascube/ansiblecubepp.git main.yml --extra-vars "generic_project_name=$PROJECT_NAME full_domain_name=$FULLDOMAIN"

ideascube runserver 8000


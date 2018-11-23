#!/bin/bash
export IDEASCUBE_ID=idb
export DOMAIN="$PROJECT_NAME.ideascube.docker.ideas-box.eu"

ideascube migrate --run-syncdb

touch /var/ideascube/kiwix/library.xml
#nohup /usr/local/bin/kiwix-serve --library --port=8002 /var/ideascube/kiwix/library.xml &

/usr/local/bin/ansible-pull -d /var/lib/ansible/local -i hosts -U https://github.com/ideascube/ansiblecubepp.git main.yml --extra-vars "generic_project_name=$PROJECT_NAME"

ideascube runserver 8000


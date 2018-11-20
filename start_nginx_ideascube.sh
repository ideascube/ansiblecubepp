#!/bin/bash

/usr/local/bin/ansible-pull -i hosts -U https://github.com/ideascube/ansiblecubepp.git main.yml --extra-vars "generic_project_name=$PROJECT_NAME"

ideascube runserver 8000

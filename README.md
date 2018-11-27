# ansiblecubepp

This ansible repo is pulled by a docker image and ansible-pull installed.

To play with this, try :
- Choose a project from https://raw.githubusercontent.com/ideascube/ansiblecube/oneUpdateFile/roles/set_custom_fact/files/device_list.fact
- `docker run -d -ti -p 80:80 -e "PROJECT_NAME=your-project-name" bibliosansfrontieres/ideascube:latest`

Note, as is, this will not work outside of BSF infrastructure.

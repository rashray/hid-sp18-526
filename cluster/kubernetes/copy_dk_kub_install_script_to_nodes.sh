#!/bin/sh

cssh -a " echo ' ' > docker_kubernites_install.sh \
 && scp pi@rp0:~/docker_kubernites_install.sh docker_kubernites_install.sh \
 && sh docker_kubernites_install.sh"
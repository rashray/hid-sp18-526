# This is a in depth exaplanion of the kubernetes installation and 
#configuration scripts


First docker needs to be installed

    curl -sSL get.docker.com \
      | sh \
      && sudo usermod pi -aG docker

Now, as docker does not work with SWAP memory it needs to be disabled, this is
easy enough 

    sudo swapoff -a 
    echo Adding " cgroup_enable=cpuset cgroup_enable=1" to /boot/cmdline.txt
    sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt

If after running this script your raspberry pi starts to not work properly 
reboot it once again, if thar does not solve the issue replace cgroup_memory=1 
with cgroup_enable=memory.

    orig="$(head -n1 /boot/cmdline.txt) cgroup_enable=cpuset cgroup_memory=1"
    echo $orig | sudo tee /boot/cmdline.txt

Now kubernetes admin will be installed 


    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - &&\
      echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list && \
      sudo apt-get update -q && \
      sudo apt-get install -qy kubeadm
    sudo reboot 

# On the nodes

Docker and kubernetes need to be installed on the nodes, as well as the SWAP 
memory needs to be disabled. This is handled by another script that simply 
copies the installation script to the nodes and runs it.  First copy the script

    for number in {1..4}
	    do 
		    scp /home/pi/docker_kubernites_install.sh \
			    pi@rp$number:/home/pi/docker_kubernites_install.sh
	    done
    exit 0

Now the installation script will be run on the nodes using cssh
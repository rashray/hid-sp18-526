# Intructions for installing kubernetes

## First install doker, disable swap, install kubeadm

All the following steps are made automatically by the 
docker_kubernetes_install.sh script.

### Install docker
In order to install kubernetes you first need to have docker installed. This is 
very strait foward.

### Disable swap memory
Docker has an issue (in my opinion severe) in that it is **not compatible with 
SWAP memory**, therefore it is neeeded to disable it. This might create some 
issues, if you encounter them you should try to rebbot the cluster again, if 
that fails change line 16 in the script from

    orig="$(head -n1 /boot/cmdline.txt) cgroup_enable=cpuset cgroup_memory=1"

to

    orig="$(head -n1 /boot/cmdline.txt) cgroup_enable=cpuset cgroup_memory=memory".

### Installing kubernetes administrator

Finally, to configure kubernetes you'll need kubeadm. Now the Pi needs to be 
rebooted.

### *All of this will be done by the script, don't worry* (maybe worry)

## For the nodes

All of the above needs to be done in each node aswell. The script
copy_dk_kub_install_script_to_nodes.sh should copy the needed script to each of 
them and run it. It is set up to work with 4 nodes named rp\<number\> with pi as 
the username (the numbers start at 1 because the head node is rp0). Changing 
the number of nodes is trivial, if all of your nodes have the same username it 
is also trivial.

If your nodes are not configured like that you'll need to change 
this script or copy docker_kubernetes_install.sh to each of the nodes manually.

## Now some more explanations on the scripts


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
      echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | \
      sudo tee /etc/apt/sources.list.d/kubernetes.list && \
      sudo apt-get update -q && \
      sudo apt-get install -qy kubeadm
    sudo reboot 

### On the nodes

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

    cssh -a "sh docker_kubernites_install.sh"

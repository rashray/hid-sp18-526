# Head Node Setup

Your head node will give you access to your compute nodes.

## Setup

The setup script will install dnsmasq for DNS/DHCP server and Cluster SSH. Cluster SSH will allow commands to be issued to one/all of the compute nodes at the same time.

Run setup script:

    sudo sh setup
    
Reboot:

    reboot
    
Run Cluster SSH:

    cssh -l pi rpcluster
    
This opens a new SSH window for each hostname in rpcluster (defined in **/etc/clusters**). Click on the gray box to type commands into each node.

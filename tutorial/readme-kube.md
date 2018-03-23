# Raspberry Pi Kubernetes Cluster

- Tim Whitson @whitstd
- Juliano Gianlupi @JulianoGianlupi

## Hardware

Each cluster consists of:

- 1 head node ([setup](head)) (recommend following the instructions here first)
- 4 compute nodes

## Configuration

### Flash Raspbian

1. Download Raspbian image <https://www.raspberrypi.org/downloads/>.
2. Download Etcher <https://etcher.io/>.
3. Using Etcher, flash Raspbian onto SD card.

### Keyboard Layout

The default keyboard layout may need to be changed to US.

Menu -> Preferences -> Mouse and Keyboard Settings -> Keyboard tab -> Variant ->
 English (US)

### Change password

Change password:

    passwd
    
Enter new password via prompts.

### Change hostnames

Change hostname of each raspberry pi (in descending order).

1. rp0
2. rp1
3. rp2
4. rp3
5. rp4

This can be done on the command line using:

    sudo raspi-config
    
Or on the desktop by going to Menu -> Preferences -> Raspbery Pi Configuration

Or by modifying **/etc/hostname**

### Configure Head Node

Install Dependencies:

    apt-get update
    apt-get install -qy dnsmasq clusterssh iptables-persistent

#### Create Static IP

Copy old config (-n flag prevents overwrite):

    \cp -n /etc/dhcpcd.conf /etc/dhcpcd.conf.old
    
To update DHCP configuration, add the following to **/etc/dhcpd.conf**:
 
    interface wlan0
    metric 200

    interface eth0
    metric 300
    static ip_address=192.168.50.1/24
    static routers=192.168.50.1
    static domain_name_servers=192.168.50.1

#### Configure DHCP Server:

Copy old config (-n flag prevents overwrite):

    \cp -n /etc/dnsmasq.conf /etc/dnsmasq.conf.old
    
To update DNS configuration, add the following to **/etc/dhcpd.conf**
    
    interface=eth0
    interface=wlan0

    dhcp-range=eth0, 192.168.50.1, 192.168.50.250, 24h

To update Cluster SSH configuration, add the following to **/etc/clusters**:

    rpcluster rp1 rp2 rp3 rp4

#### NAT Forwarding

To Setup NAT Forwarding, uncomment ipv4 fowarding:

    sed -i -e "/net.ipv4.ip_forward=1/s/^#//" /etc/sysctl.conf
    
#### IP Tables

Create IP Tables:

    sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i $INTERNAL -o wlan0 -j ACCEPT
    sudo iptables -A FORWARD -i $EXTERNAL -o eth0 -j ACCEPT

Make rules permanent:

    iptables-save > /etc/iptables/rules.v4

### SSH

**Note: Gregor says this is not best practice**

Generate SSH keys:

    ssh-keygen -t rsa
    
Copy key to each node:

    ssh-copy-id <hostname>
    
For hostnames rp1-4.

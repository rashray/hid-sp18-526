# Head Node Setup

Your head node will give you access to your compute nodes.

## Configuration

### Flash Raspbian

1. Download Raspbian image [here](https://www.raspberrypi.org/downloads/).
2. Download Etcher here [here](https://etcher.io/).
3. Using Etcher, flash Raspbian onto SD card.

### Update

Update:

    sudo apt-get update
    
### DHCP Server

Credit goes to [Makezine](https://makezine.com/projects/build-a-compact-4-node-raspberry-pi-cluster/)

Install:

    sudo apt-get install isc-dhcp-server
    
Change **/etc/dhcp/dhcpd.conf** to (inserting MAC address):

```
ddns-update-style none;
authoritative;
log-facility local7;

# No service will be given on this subnet
subnet 192.168.1.0 netmask 255.255.255.0 {
}

# The internal cluster network
group {
   option broadcast-address 192.168.50.255;
   option routers 192.168.50.1;
   default-lease-time 600;
   max-lease-time 7200;
   option domain-name "cluster";
   option domain-name-servers 8.8.8.8, 8.8.4.4;
   subnet 192.168.50.0 netmask 255.255.255.0 {
      range 192.168.50.14 192.168.50.250;

      host rp0 {
         hardware ethernet (MAC address);
         fixed-address 192.168.50.1;
      }
      
      host rp1 {
         hardware ethernet (MAC address);
         fixed-address 192.168.50.11;
      }
      
      host rp2 {
         hardware ethernet (MAC address);
         fixed-address 192.168.50.12;
      }
      
      host rp3 {
         hardware ethernet (MAC address);
         fixed-address 192.168.50.13;
      }
      
      host rp4 {
         hardware ethernet (MAC address);
         fixed-address 192.168.50.14;
      }
   }
}
```

This assigns static IPs to each node.

Change **/etc/default/isc-dhcp-server** to:

```
DHCPD_CONF=/etc/dhcp/dhcpd.conf
DHCPD_PID=/var/run/dhcpd.pid
INTERFACES="eth0"
```

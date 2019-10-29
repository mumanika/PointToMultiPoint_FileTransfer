#!/bin/bash

cp p2mpUdpServer_Final.py /usr/bin/p2mpserver
cd /usr/bin/
chmod +x p2mpserver
export PATH > .profile
source .profile
iptables -F
cd ~


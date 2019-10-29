#!/bin/bash

cp p2mpudpClient.py /usr/bin/p2mpudpClient.py
cp p2mpudpClientFinal.py /usr/bin/p2mpclient

cd /usr/bin/
chmod +x p2mpudpclient
export PATH > .profile
source .profile
iptables -F
cd ~
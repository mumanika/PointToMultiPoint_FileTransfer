#!/usr/bin/env python

import sys
import struct
import binascii 
import socket
import ipaddress
import p2mpudpClient as Client
import threading
import datetime,csv,time


def SendToServer(i,ServerPort,Filename,MSS):
	
	Server=i
	c=Client.Client(i,ServerPort,FileName,MSS)
	
	
	seq=0
	timeStart=datetime.datetime.now()
	with open(c.FileName, "r") as f:
		Data=f.read(c.MSS)
		while Data:
			CheckSum=c.CheckSum(Data)
			Packet=c.MakePacket(seq,CheckSum,Data)
			c.rdt_send(Packet, struct.unpack('!LHH',Packet[:8])[0])
			seq=seq+1
			Data=f.read(c.MSS)
		f.close()
	Checksum=c.CheckSum(str(0b0101010101010101))
	Packet=c.MakePacket(seq,CheckSum,str(0b0101010101010101))
	c.rdt_send(Packet, struct.unpack('!LHH',Packet[:8])[0])
	timeEnd=datetime.datetime.now()
	


	'''
	List=c.DataSplitter()
	seq=0
	FinalPacketList=[]
	for i in List:
		CheckSum=c.CheckSum(i)
		FinalPacketList.append(c.MakePacket(seq,CheckSum,i))
		seq=seq+1
	timeStart=datetime.datetime.now()
	for i in FinalPacketList:
		c.rdt_send(i, struct.unpack('!LHH',binascii.unhexlify(i[:16]))[0])
	timeEnd=datetime.datetime.now()
	'''
	
	
	print "\n",Server, (timeEnd-timeStart).total_seconds()
	
	with threading.Lock():
		f=open("Downloadtime.csv","a+")
		w=csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		w.writerow([str(Server),str((timeEnd-timeStart).total_seconds())])
		f.close()
	

ServerList = []
Remaining=[]
args=sys.argv
args.pop(0) # To remove the /root/bin/<command-name>


for arg in args:
    try:
        ipaddress.ip_address(unicode(arg, "utf-8"))
        ServerList.append(arg)
    except ValueError:
        Remaining.append(arg)


ServerPort = int(Remaining.pop(0))
FileName = Remaining.pop(0)
MSS = int(Remaining.pop(0))



for i in ServerList:
	x=threading.Thread(target=SendToServer, args=(i,ServerPort,FileName,MSS,))
	x.daemon=True
	x.start()
	
while threading.active_count() !=1:
	time.sleep(0.5)



#!/usr/bin/env python

import sys
import socket
import binascii
import random,struct
	
class Server:
	def __init__(self,ServerPort=7735, FileName="ReceivedFile.txt", ProbLoss=0):
		self.ServerPort=ServerPort
		self.ServerSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.FileName=FileName
		self.ServerSocket.bind(('',self.ServerPort))
		self.ProbLoss=ProbLoss
		
	def ComputeCheckSum(self, DataPacket):
		'''
		This function is responsible to calculate the checksum of the DataPacket. 
		The function responsibilities are: 
			Split the data packet into chunks of 16bits.
			Perform a binary addition with carryover for all of these 16 bit chunks.
		Inputs: 
			DataPacket: String of data, packet to a maximum of MSS-8 bytes.
		Outputs: 
			Checksum value as an Int type
		'''
		DataPacket=binascii.hexlify(DataPacket)
		sum=0
		for i in range(0, len(DataPacket), 2):
			DoubleWord=ord(DataPacket[i]) + (ord(DataPacket[i+1])<<8)
			sum=self.Add_CarryAround(sum,DoubleWord)
		return sum & 0xffff
		
	def Add_CarryAround(self, a, b):
		'''
		This function is used by CheckSum to add two numbers.
		'''
		c=a+b
		return (c & 0xffff) + (c >> 16)
		
	def MakePacket(self, SequenceNumber):
		'''
		This function will be used in order to make every packet that is to be sent to the client.
		The function responsibilities are:
			Pack the SequenceNumber, the 16bit value of all 0's and a 16 bit field that has a value of 1010101010101010.
		Inputs: 
			SequenceNumber : integer, packed t0 32 bits
		Outputs:
			Packet that is ready for sending through the socket.
		'''
		FinalPacket = struct.pack('!LHH',SequenceNumber,0,0b1010101010101010)
		return FinalPacket
		
	def GenerateNumber(self):
		'''
		This function will be used in order to generate a number that ranges between 0 and 1.
		This will be used in order to determine the probabilistic loss simulation. 
		The function responsibilities are: 
			Generate a random number between 0 and 1, and return this value. 
		Inputs: 
			None
		Outputs:
			Int value between 0 and 1
		'''
		return random.uniform(0,1)
		
	def WriteToFile(self, Data):
		'''
		This function is used to write the data that is reecived to a file. 
		Function responsibilities:
			Open the file in append mode. 
			Write the data to the file.
			Close the file.
			Return True if write is completed. 
			
		Function Inputs:
			Data that is to be writted to the file.
			
		Function Outputs:
			True if write operation is complete. False if write operation is not complete.
		'''
		
		try:
			with open(self.FileName, "a+") as f:
				f.write(Data)
			f.close()
			return True
		except:
			return False
			
	def StartServer(self):
		'''
		This function will receive the data packet from the client, starting from sequence 0. The checksum is computed, and if the packet is in sequece, it is written to the file. 
		There is a probability implementation as well where function will simply drop the packet if a random number is less than that provided by the user. 
		Function Responsibilities:
			Start with sequence 0 and read a packet. 
			Generate a random value between 0 and 1 and compare with the probability value supplied by the user. If lesser, drop the pakcket and repeat. Else, continue.
			Compute the checksum and check if the packet is in sequence. If yes, then write the data to the file and send the ACK. 
			If Checksum is okay but the packet is out of order, send ACK back for the expected sequence.
			If the Checksum is not correct, then just continue the loop.
			
		'''
		
		seq=0
	
		while True:
			Data, client=self.ServerSocket.recvfrom(4096)
			Header=Data[:8]
			RandNum=round(self.GenerateNumber(),2)
			if RandNum <= self.ProbLoss:
				print "Packet loss, sequence number = {}".format(str(seq))
				continue
			List=struct.unpack('!LHH',Header)
			DataPacket=Data[8:]
			VerificationSum=self.Add_CarryAround(self.ComputeCheckSum(DataPacket),List[1])
			if (List[0]) == seq and (VerificationSum==65535) and not(DataPacket.endswith("21845")):
				self.WriteToFile(DataPacket)
				FinalPacket=self.MakePacket(seq)
				self.ServerSocket.sendto(FinalPacket,client)
				seq=seq+1
			elif (List[0]) != seq and (VerificationSum==65535):
				if seq-1 < 0:
					FinalPacket=self.MakePacket(0)
					self.ServerSocket.sendto(FinalPacket,client)
					
				else:
					FinalPacket=self.MakePacket(seq-1)
					self.ServerSocket.sendto(FinalPacket,client)
			elif DataPacket.endswith("21845"):
				FinalPacket=self.MakePacket(seq)
				self.ServerSocket.sendto(FinalPacket,client)
				break
			else: 
				continue
			
			
		
	

args=sys.argv
#print args
args.pop(0) # To remove the /root/bin/<command-name>

ServerPort = int(args.pop(0))
FileName = args.pop(0)
ProbLoss = round(float(args.pop(0)),2)

'''
print(ServerPort)
print(FileName)
print(ProbLoss)
'''

s=Server(ServerPort,FileName,ProbLoss)
s.StartServer()		

'''	
address=('',7735)
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

while True:
	data, server = s.recvfrom(4096)
	print data,server
	print binascii.unhexlify(data)
'''	

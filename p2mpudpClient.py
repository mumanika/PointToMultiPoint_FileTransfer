import socket, binascii, struct

class Client():
	def __init__(self, ServerIP='10.0.0.9', ServerPort=50000, FileName="TestFile.txt", MSS=500):
		self.ServerIP=ServerIP
		self.ServerPort=ServerPort
		self.FileName=FileName
		self.ServerAddress=(self.ServerIP, self.ServerPort)
		self.ClientSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#self.ClientSocket.bind(('',25000))
		self.MSS=MSS
		self.AckFlag=False
		
	def MakePacket(self, SequenceNumber, CheckSum, DataPacket):
		'''
		This function will be used in order to make every packet that is to be sent to a server.
		The function responsibilities are:
			Pack the SequenceNumber, the 16bit Checksum and the data packet.
		Inputs: 
			SequenceNumber : integer, packed t0 32 bits
			CheckSum : integer packed to 16 bits
			DataPacket: packed to a maximum of MSS bytes
		Outputs:
			Packet that is ready for sending through the socket.
		'''
		Header= struct.pack('!LHH',SequenceNumber,CheckSum,0b0101010101010101)
		FinalPacket=Header+DataPacket
		return FinalPacket
		
		
	def CheckSum(self, DataPacket):
		'''
		This function will be responsible to caclculate the checksum of the data portion of the packet. 
		The function responsibilities are: 
			Split the data packet into chunks of 16bits.
			Perform a binary addition with carryover for all of these 16 bit chunks.
		Inputs: 
			DataPacket: String of data, packet to a maximum of MSS bytes.
		Outputs: 
			Checksum value as an Int type
		Link to check implemetation: https://stackoverflow.com/questions/1767910/checksum-udp-calculation-python
		'''
		DataPacket=binascii.hexlify(DataPacket)
		sum=0
		for i in range(0, len(DataPacket), 2):
			DoubleWord=ord(DataPacket[i]) + (ord(DataPacket[i+1])<<8)
			sum=self.Add_CarryAround(sum,DoubleWord)
		return ~sum & 0xffff
		
	def Add_CarryAround(self, a, b):
		'''
		This function is used by CheckSum to add two numbers.
		'''
		c=a+b
		return (c & 0xffff) + (c >> 16)
		
	def DataSplitter(self):
		'''
		This function will read the file that is provided by the user and split the data into the MSS bytes chunks.
		The functin responsiilities are: 
			Read the data from the file.
			Split the data into chunks of MSS bytes.
			Append these chunks to a list data structure.
		Inputs: 
			Filename: Can be taken from the member variable of the class.
		Outputs:
			List containing the split file.
		'''
		List=[]
		with open(self.FileName, "r") as f:
			Data=f.read(self.MSS)
			while Data:
				List.append(Data)
				Data=f.read(self.MSS)
			f.close()
		List.append(str(0b0101010101010101))
		return List
		
		
	def rdt_send(self, FinalPacket, seq):
		'''
		This funtction will send the packet out to the destined server.
		Function responsibilities:
			Send the packet out to the server. 
			Wait for the acknowledgement packet. 
			Trigger a resend if the timer expires. 
			
		'''
		
		while True:
			try:
				self.ClientSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				self.ClientSocket.sendto(FinalPacket,(self.ServerIP,self.ServerPort))
				self.ClientSocket.settimeout(0.5)
				data, server= self.ClientSocket.recvfrom(4096)
				#Need to configure logic for ACK Packets
				List=struct.unpack('!LHH',data)
				if List[0]==seq and List[2]==0b1010101010101010:
					break
				elif List[0]!=seq or List[2]!=0b1010101010101010:
					continue
			except socket.timeout:
				print "Timeout, sequence number = {}\n".format(str(seq))
				continue
				
			
			
'''		
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

String="Hey, my name is mukul"
print binascii.hexlify(String)
print binascii.unhexlify(binascii.hexlify(String))

s.sendto(binascii.hexlify(String),('10.0.0.9',50000))

	
c=Client()
DataPacket="a"
Checksum=c.CheckSum(binascii.hexlify(DataPacket))
sum = 0
for i in range(0, len(binascii.hexlify(DataPacket)), 2):
	DoubleWord=ord(binascii.hexlify(DataPacket)[i]) + (ord(binascii.hexlify(DataPacket)[i+1])<<8)
	sum=c.Add_CarryAround(sum,DoubleWord)
	verficationSum=c.Add_CarryAround(sum,Checksum)
	
print binascii.hexlify(struct.pack('!L',Checksum))
x=c.MakePacket(12345,Checksum,DataPacket)
print "size", x[:16]
'''


		



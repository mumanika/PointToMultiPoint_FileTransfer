####################### Readme p2mpudp File Transfer #######################

Instructions to run the program: 

> The scripts are coded in python 2.7. Therefore, please ensure that your systems have Python 2.7 installed. 
> Untar the file and place the contents of the Server Files to any directory of your choice on the system designated to be the server. The same needs to be done with the Client files for the Client machine. 
> Provide executable permissions using "sudo chmod +x MakeFileServer.sh" and "sudo chmod +x MakeFileClient.sh" on the server and client machines respectively. 
> Run the scripts as root using the command "sudo ./MakeFileServer.sh" and "sudo ./MakeFileClient.sh" respectively. This will get the environment ready for the file transfer program.

Commands on Server once setup is complete: 
p2mpserver <Server Port> <File Name with path if needed> <Loss Probability>

Commands on the Client once the setup is complete: 
p2mpclient <Server IP(s) to send file to separated by spaces> <Server Port> <File name to transfer> <MSS value>

> The program will exit once the file transfer is complete. 

Authors: 
------------------------------------
Mukul Manikandan (mmanika@ncsu.edu)
Akhil Nidumukkula (anidumu@ncsu.edu)

####################### Readme p2mpudp File Transfer #######################

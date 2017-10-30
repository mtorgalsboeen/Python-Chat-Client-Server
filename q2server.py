import socket                                         
import time
import threading
import select

port = 9012

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                                                                   

# bind to the port
serversocket.bind((host, port));                                  
serversocket.listen(2); 
clientSockets = [];
resultList = [None] * 2;                              

print("**********Chat Service**********");
print("Waiting for client connections.");

for x in range(0, 2):
    # establish a connection
    clientsocket,addr = serversocket.accept() ;
    clientSockets.append(clientsocket);
    print("A user connected with server");

print("Starting chat service.");
clientSockets[0].sendall(b"ready");
clientSockets[1].sendall(b"ready");
print("Started chat service.");

exit = False;

while not exit:
	readable, writable, exceptional = select.select(clientSockets, [], clientSockets);

	for s in readable:
		data = s.recv(1024);

		if data.decode('utf-8').strip().lower() == "bye":
			exit = True;

		if s == clientSockets[0] or exit:
			clientSockets[1].send(data);
		
		if s== clientSockets[1] or exit:
			clientSockets[0].send(data);

print("Chat service terminated.");
clientSockets[0].close();
clientSockets[1].close();
serversocket.close();
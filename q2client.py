
import socket
import threading
import sys
import os

port = 9012;
userName = "";

def clientSocketThread(sock, event):
	while True:
		data = sock.recv(1024);
		
		if(data.decode('utf-8').strip().lower() == "bye"):
			event.set();
			return;
		else:
			print(data.decode('utf-8'));

def clientInputThread(sock, userName, event):
	while True:
		msg = input();

		if(msg.strip().lower() != "bye"):
			msg = userName + ": " + msg;

		sock.sendall(msg.encode('utf-8'));

		if(msg.strip().lower() == "bye"):
			event.set();
			return;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
event = threading.Event();

host = socket.gethostname();                          

print("**********Chat Service**********");
while not (userName == "bob" or userName == "alice"):
	userName = input("What's your name (Bob or Alice)? ");
	userName = userName.strip().lower();

#otherUser = "Bob" if (userName == "alice") else "Alice"
userName = userName.title();

s.connect((host, port));

print("Connected with server, waiting to initiate chat service.")
data = s.recv(1024);
ackSignal = "";

while ackSignal != "ready":
	ackSignal = data.decode('utf-8');

print("Chat service started.");
print("Type bye to exit or message to sent.\n");

inputThread  = threading.Thread(target=clientInputThread, args=(s,userName, event));
socketThread = threading.Thread(target=clientSocketThread, args=(s, event))

inputThread.start();
socketThread.start();

event.wait();

print("Chat service terminated.");
s.close();

os._exit(1);
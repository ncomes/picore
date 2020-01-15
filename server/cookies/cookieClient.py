import socket

host = '169.254.121.158'
port = 5560

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_SOCKET.connect((host, port))

while True:
	command = input('Enter your command: ')
	if command == 'EXIT':
		# Send Exit request to other end
		SERVER_SOCKET.send(str.encode(command))
		break
	elif command == 'KILL':
		# Send Kill command
		SERVER_SOCKET.send(str.encode(command))
		break
	SERVER_SOCKET.send(str.encode(command))
	reply = SERVER_SOCKET.recv(1024)
	print(reply.decode('utf-8'))
	
SERVER_SOCKET.close()
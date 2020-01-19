import datetime
import socket
import time

#HOSTS = ['192.168.86.212']
#PORT = 5560

def socket_connection(host, port):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.connect((host, port))
	return server_socket


def send_command(hosts, port, command=''):
	if not command or command == '':
		return
	elif command == 'PHOTO':
		message = 'Photo Captures Complete.\n'
	elif command == 'SHUTDOWN':
		message = 'Shutting Down:\n'
	elif command == 'KILL':
		message = 'Stoppping Server.\n'
	start_time = time.time()
	for host in hosts:
		server_socket = socket_connection(host, port)
		server_socket.send(str.encode(command))
		server_socket.close()
	print('All completed.\n')
	message = 'Photo Captures Completed.\n'
	time_elapsed = str(datetime.timedelta(seconds=time.time() - start_time))
	print(message + 'Time Elapsed: ' + time_elapsed)
	return



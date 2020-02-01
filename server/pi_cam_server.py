#! /usr/bin/python3
import sys
main_path = r'/home/pi/picore'
sys.path.append(main_path)

import socket
# import photo.capture as take_photo
from subprocess import call
import pi_cam
import time
import os
import ssh.ssh_connect as ssh_client
import git_handler.git_commands as git_client
#import ssh.ssh_connect as ssh_client

HOST = ''
PORT = 5560
PHOTO_PATH = r'/home/pi/pictures'

def setup_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print('Socket created...')
	try:
		server_socket.bind((HOST, PORT))
	except socket.error as msg:
		print(msg)
	
	print('Socket bind complete')
	
	return server_socket


def setup_connection():
	server_socket = setup_server()
	server_socket.listen(1)  # allows one connection
	conn, address = server_socket.accept()
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	return [conn, server_socket]


def data_name(data):
	data_message = data.split(' ', 1)
	commands = [data_message[0]]
	data_len = len(data_message)
	if data_len > 1:
		for x in range(1, data_len):
			commands.append(data_message[x])
	hostname, ip_address = get_ip_address()
	#ip_name = str(ip_address.split('.')[-1])
	ip_name = hostname
	commands.append(ip_name)
	return commands

def git_pull():
	git_dir = r'/home/pi/picore'
	git_commands = git_client.GitClient()
	git_commands.pull(git_dir)
	return

def get_ip_address():
	hostname = socket.gethostname()
	print(hostname)
	ip_address = socket.gethostbyname(hostname)
	print(ip_address)
	return [hostname, ip_address]

def send_file(file_name):
	full_file_name = os.path.join(PHOTO_PATH, file_name)
	ssh_client.ssh_send_file(full_file_name, full_file_name, 'pi', 'piDepot')
	#ssh = ssh_client.SSHClient()
	#ssh.open_connection(hostname='piDepot01.local',
	#					username='pi',
	#					pswd='piDepot')
	#ssh.send_file(full_file_name, full_file_name)
	#ssh.close_connection()
	return

def data_transfer(connection):
	'''
	Big loop that sends/recieves data until told not to.
	:param conn:
	:return:
	'''
	stored_value = "Server is listening..."
	conn = connection[0]
	server_socket = connection[1]
	while True:
		# Receive the data
		data = conn.recv(1024)  # receive the data
		data = data.decode('utf-8')
		# Split the data that you separate the command
		# from the rest of the data.
		data_message = data_name(data)
		#data_message = data.split(' ', 1)
		command = data_message[0]
		file_name = data_message[1] + '_' + data_message[-1] + '.jpg'
		reply = ''
		if command == 'PHOTO':
			pi_cam.pi_cam_still(name=file_name,
								path=PHOTO_PATH)
			print('Finishing taking photos...\n')
			time.sleep(1)
			send_file(file_name)
			server_socket.close()
			break
		elif command == 'TEST':
			reply = stored_value
		elif command == 'EXIT':
			print('Client has ended.')
			break

		elif command == 'KILL':
			print('Server is stopping...')
			server_socket.close()
			conn.close()
			raise RuntimeError('Stopped Server...')

		elif command == 'SHUTDOWN':
			print('Pi is shutting down...')
			server_socket.close()
			conn.close()
			call('sudo shutdown -h now', shell=True)
			break
		elif 'GITPULL' in command:
			print('Getting latest')
			git_pull()

		elif 'REBOOT' in command:
			server_socket.close()
			conn.close()
			call('sudo reboot', shell=True)

		else:
			reply = 'Unknown Command'
		conn.sendall(str.encode(reply))
		print('Data has been sent.')
	conn.close()


def start():
	print('STARTING!')
	while True:
		try:
			conn = setup_connection()
			data_transfer(conn)
		except Exception as e:
			print(e)
			break
	print('start() has stopped!')


start()

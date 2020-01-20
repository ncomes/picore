import socket
# import photo.capture as take_photo
from subprocess import call
import pi_cam

HOST = ''
PORT = 5560


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
		data_message = data.split(' ', 1)
		command = data_message[0]
		reply = ''
		if command == 'PHOTO':
			cam_path = pi_cam.pi_cam_still()
			print('Finishing taking photos...\n')
			print(cam_path)
			server_socket.close()
			conn.close()
			#time.sleep(2)
			start()
		elif command == 'TEST':
			reply = stored_value
		elif command == 'EXIT':
			print('Client has ended.')
			break
		elif command == 'KILL':
			print('Server is stopping...')
			server_socket.close()
			conn.close()
			break
		elif command == 'SHUTDOWN':
			print('Pi is shutting down...')
			server_socket.close()
			conn.close()
			call('shutdown -h now', shell=True)
			break
		elif 'GITPULL' in command:
			call('git pull')
		else:
			reply = 'Unknown Command'
		conn.sendall(str.encode(reply))
		print('Data has been sent.')
	conn.close()


# SERVER_SOCKET = setup_server()s
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

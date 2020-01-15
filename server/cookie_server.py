import socket
# import photo.capture as take_photo
import time
from subprocess import call
import datetime

HOST = ''
PORT = 5560

stored_value = "Voltron!!!"

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


def take_photos():
	capture_all()
	return


def capture_one(image_name=r'/home/pi/temp_image.png', video_path=r'/dev/video0'):
	call(['fswebcam',
		'-d',
		video_path,
		'-r',
		'720x480',
		# '1080x720',
		'--no-banner',
		image_name])
	print(video_path + ': Photo at: ' + str(datetime.datetime.now()))
	return


def capture_all():
	start_time = time.time()
	capture_one(image_name=r'/home/pi/temp_image_01.png', video_path=r'/dev/video0')
	# capture_one(image_name=r'/home/pi/temp_image_02.png', video_path=r'/dev/video2')
	
	message = 'Photo Captures Completed. '
	time_elapsed = str(datetime.timedelta(seconds=time.time() - start_time))
	print(message + 'Time Elapsed: ' + time_elapsed)
	return


def data_transfer(connection):
	'''
	Big loop that sends/recieves data until told not to.
	:param conn:
	:return:
	'''
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
			take_photos()
			print('Finishing taking photos...')
			server_socket.close()
			conn.close()
			time.sleep(2)
			start()
			
		elif command == 'EXIT':
			print('Client has ended.')
			break
		elif command == 'KILL':
			print('Server is shutting down...')
			server_socket.close()
			break
		elif command == 'SHUTDOWN':
			print('Pi is shutting down...')
			server_socket.close()
			break
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

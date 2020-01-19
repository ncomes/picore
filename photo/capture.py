from subprocess import call
import datetime
import time
from picamera import PiCamera
import os


def capture(image_name='temp_image', video_path='/dev/video0'):
	#dt = datetime.datetime.now()
	#dtime = dt[0:4]+dt[5:7]
	call(['fswebcam', '-d', '/dev/video0', '-r', '720x480','/home/pi/testcam_01_image1.jpg'])
	print(datetime.datetime.now())
	call(['fswebcam', 
	'-d', 
	'/dev/video2', 
	'-r', 
	'3456x2304', 
	#'1080x720', 
	'--no-banner', 
	'/home/pi/testcam_02_image1.png'])
	print(datetime.datetime.now())


def capture_one(image_name=r'/home/pi/temp_image_03.png', video_path=r'/dev/video0'):
	call(['fswebcam',
	'-d',
	video_path,
	'-r',
	'1080x720',
	#'1080x720',
	'--no-banner',
	image_name])
	print(video_path + ': Photo at: ' + str(datetime.datetime.now()))
	return

def capture_all():
	start_time = time.time()
	capture_one(image_name=r'/home/pi/temp_image_01.png', video_path=r'/dev/video0')
	capture_one(image_name=r'/home/pi/temp_image_02.png', video_path=r'/dev/video2')
	
	message = 'Photo Captures Completed. '
	time_elapsed = str(datetime.timedelta(seconds=time.time() - start_time))
	print(message + 'Time Elapsed: ' + time_elapsed)
	return

#capture_one()

def pi_cam_still(name='picture.jpg', path=r'/home/pi/pictures', preview=False, preview_time=5):
	camera = PiCamera()
	if not os.path.isdir(path):
		os.mkdir(path)
		call(['sudo chown pi ' + path])
	if preview:
		camera.start_preview()
		time.sleep(preview_time)
	camera.capture(os.path.join(path, name))
	if preview:
		camera.stop_preview()
	return os.path.join(path, name)

pi_cam_still()
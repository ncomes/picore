from subprocess import call
import datetime
import time
from picamera import PiCamera
import os


def pi_cam_still(name='picture.jpg', path=r'/home/pi/Desktop', preview=False, preview_time=5):
	camera = PiCamera()
	if preview:
		camera.start_preview()
		time.sleep(preview_time)
	camera.capture(os.path.join(path, name))
	if preview:
		camera.stop_preview()
	return os.path.join(path, name)


#pi_cam_still()
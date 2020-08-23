import datetime
import time
from picamera import PiCamera
import os


def pi_cam_still(name, path):
	camera = PiCamera()
	camera.capture(os.path.join(path, name))
	camera.close()
	return os.path.join(path, name)


#pi_cam_still()

def legacy_pic_cam_still(name, path, preview_time=1.0):
	camera = PiCamera()
	camera.resolution(2592, 1944)
	camera.resolution(2688, 1520)
	camera.preview_fullscreen=False
	camera.start_preview()
	time.sleep(preview_time)
	camera.capture(os.path.join(path, name))
	camera.stop_preview()
	camera.close()
	return os.path.join(path, name)


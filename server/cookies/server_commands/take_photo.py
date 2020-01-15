from subprocess import call
import datetime
import time


def capture():
	# dt = datetime.datetime.now()
	# dtime = dt[0:4]+dt[5:7]
	call(['fswebcam', '-d', '/dev/video0', '-r', '720x480', '/home/pi/testcam_01_image1.jpg'])
	print(datetime.datetime.now())
	call(['fswebcam',
			'-d',
			'/dev/video2',
			'-r',
			'3456x2304',
			# '1080x720',
			'--no-banner',
			'/home/pi/testcam_02_image1.png'])
	print(datetime.datetime.now())




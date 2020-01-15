import datetime
from subprocess import call
import time



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



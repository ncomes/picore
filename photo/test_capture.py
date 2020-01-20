import capture

PHOTO_PATH = r'/home/pi/Desktop'

capture.pi_cam_still(name='picture.jpg',
                        path=PHOTO_PATH,
                        preview_time=0)
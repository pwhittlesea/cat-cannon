# -*- coding: utf-8 -*-

from time import sleep
from picamera import PiCamera

# Explicitly open a new file called my_image.jpg
my_file = open('my_image.jpg', 'wb')

# Create the camera object
camera = PiCamera()
camera.start_preview()

# Camera warm-up time
sleep(2)

# Save the image to a file
camera.capture(my_file)
my_file.close()

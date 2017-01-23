# -*- coding: utf-8 -*-

import io
import random
import picamera
from time import sleep
from PIL import Image, ImageFilter, ImageChops, ImageDraw

prev_image = None

def captureImage(camera, image_path):
    """
    Capture an image and apply the necessary filters and conversion to the given image.
    """
    image_stream = io.BytesIO()
    camera.capture(image_stream, format='jpeg', use_video_port=True)
    image_stream.seek(0)
    image = Image.open(image_stream).convert("L").filter(ImageFilter.BLUR)

    # Allow debug of images by storing to an optional path
    if image_path is not None:
        image.save(image_path)
    
    return image

def draw_crosshair(image):
    width, height = image.size
    center_x = width / 2
    center_y = height / 2

    draw = ImageDraw.Draw(image)
    draw.line((center_x - 20, center_y, center_x + 20, center_y), fill=128, width=10)
    draw.line((center_x, center_y - 20, center_x, center_y + 20), fill=128, width=10)
    del draw

def merge_images(image1, image2):
    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    return result

def detect_motion(camera):
    """
    Capture an image and compare it to the given previous image for motion.
    Return true if motion was detected.
    """
    global prev_image
    current_image = captureImage(camera, "images/current.jpg")

    if prev_image is None:
        prev_image = current_image
        return False
    else:
        # Compare current_image to prior_image to detect motion.
        difference_image = ImageChops.difference(prev_image, current_image)
        motion_image = Image.eval(difference_image, lambda x: 255*(x>27.5) )
        ImageDraw.Draw(motion_image).rectangle(((0,0),(10,10)), outline = "red")
        motion_image.save("images/diff.jpg")

        merge_images(prev_image, merge_images(current_image, merge_images(difference_image, motion_image))).save("images/overview.jpg")

        # Save current image to previous image
        prev_image = current_image

        # Was motion detected?
        return random.randint(0, 10) == 0

with picamera.PiCamera() as camera:
    camera.resolution = (800, 600)
    camera.rotation = 180
    camera.iso = 100

    # Wait for the automatic gain control to settle
    sleep(2)

    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    
    stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_recording(stream, format='h264')

    try:
        while True:
            camera.wait_recording()
            if detect_motion(camera):
                print('Motion detected!')
                stream.clear()

                # Here we will move the crosshair over the change and fire the water cannon
                print('Moving')
                print('Firing')

                # Wait until motion is no longer detected, then split recording back to the in-memory circular buffer
                while detect_motion(camera):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()

'''
    Project : Autonomous Driving
    Developer : Song Chi Heon, Hyun Chung Hwan, Geum Dong Il

    [Function]
    1. Lane Following Assist
    2. Detect red traffic light and stop.
    3. Detect stop line and stop.

    [Hardware Specification]
    1. C920 Logitech Camera Cam
    2. Latte Panda or Raspberry Pi Model 3 B+ --> For Computer Vision
    3. Arduino and Motor
    4. Nice Car :)

    If you have any question, please feel free to contact me : jimm5673@gmail.com
'''
import numpy as np
import cv2
import math
import time
import os
import serial
from PIL import Image
import time
import subprocess
import RPi.GPIO as GPIO
from twython import Twython

##img = cv2.VideoCapture('/home/pi/Downloads/lastYear.mp4')
img = cv2.VideoCapture(0)
SCREEN_WIDTH = 1280  # Screen Width
SCREEN_HEIGHT = 720  # Screen Height
IMG_WIDTH = "1280"
IMG_HEIGHT = "720"
IMG_NAME = "tweet-pic.jpg"
photo_signal = 0
cnt = 0
ser = serial.Serial('/dev/ttyACM0',115200)

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)
SYSTEM_RUNNING = 23 # indicates that program is running

GPIO.setup(SYSTEM_RUNNING, GPIO.OUT) 
##GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# your twitter app keys goes here
apiKey = 'sVRtTTKDh7lrm72Z5IK74g7jx' # put twitter API Key here
apiSecret = 'wW7XnxlMYCW3zh0nuiZ81yC1GM1B7XveHHbzbUplziNIQiUMuK' # put twitter API Secret here
accessToken = '1023246194883973121-Pepn8fOVP9XJaPyVQASMPwlxvsZpND' # twitter access token here
accessTokenSecret = 'V35R5fLADIwWb1ZYd5uKkr4UZGe6Ct0I7Rpq6uVi1tMuO' # twitter access token secret

# this is the command to capture the image using pi camera
snapCommand = "raspistill -w " + IMG_WIDTH +  " -h " + IMG_HEIGHT + " -o " + IMG_NAME

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

GPIO.output(SYSTEM_RUNNING, False) # working LED to off
print("System Ready - push button to take picture and tweet.\n")


try:

    newpath = '/home/pi/smart_car/arduino/joystick/joystick_savingmovement_2servo/photo'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!")
        raise


def capcap():
    if ser.readable():
        global cnt
        if cnt == 0:
       
            try:
                print(str(ser.readline()))
                photo_signal = int(ser.readline())
                cnt += 1
                #print("photo : " + str(photo_signal))
                
                
                if photo_signal == 1 :
                    #cv2.imshow('frame',crop_image)
                    cv2.imwrite('/home/pi/smart_car/arduino/joystick/joystick_savingmovement_2servo/photo/tweet-pic.jpg',crop_image)

                    print("Program running...\n")
                    GPIO.output(SYSTEM_RUNNING, True)

                    print("Capturing photo...\n")
                    ret = subprocess.call(snapCommand, shell=True)
                    photo = open('/home/pi/smart_car/arduino/joystick/joystick_savingmovement_2servo/photo/tweet-pic.jpg', 'rb')

                    print("Uploading photo to twitter...\n")
                    media_status = api.upload_media(media=photo)

                    time_now = time.strftime("%H:%M:%S") # get current time
                    date_now =  time.strftime("%d/%m/%Y") # get current date
                    tweet_txt = "Photo captured by @twybot at " + time_now + " on " + date_now

                    print("Posting tweet with picture...\n")
                    api.update_status(media_ids=[media_status['media_id']], status=tweet_txt)

                    #deprecated method replaced by upload_media() and update_status()
                    #api.update_status_with_media(media=photo, status=tweetStr)

                    GPIO.output(SYSTEM_RUNNING, False) 
                    print("Done - System ready again.\n")
                        


                elif photo_signal == 0:
                    cnt = 0
                    cv2.imshow('frame', crop_image)
                    
            
            except KeyboardInterrupt:
                GPIO.output(SYSTEM_READY_LED,False)
                GPIO.cleanup()

while (True):
    ret, bgr_image = img.read()

    crop_image = bgr_image[0:SCREEN_HEIGHT, 0:SCREEN_WIDTH]
    capcap()
    
    if cv2.waitKey(1) & 0xFF == ord('q') :
            print ("interrupt!")
            



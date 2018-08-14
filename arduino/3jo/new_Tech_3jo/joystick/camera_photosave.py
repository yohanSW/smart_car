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


try:

    newpath = '/home/pi/Desktop/smart_car/arduino/3jo/new_Tech_3jo/joystick/photo'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!")
        raise


def capcap():
    if ser.readable():
       
        try:
            print(str(ser.readline()))
            photo_signal = int(ser.readline().decode())
       
            #print("photo : " + str(photo_signal))
            
            
            if photo_signal == 1 :
                #cv2.imshow('frame',crop_image)
                cv2.imwrite('/home/pi/Desktop/smart_car/arduino/3jo/new_Tech_3jo/joystick/photo/tweet-pic.jpg',crop_image)


            elif photo_signal == 0:
                cv2.imshow('frame', crop_image)

        except ValueError:
            pass

                    
while (True) :
    ret, bgr_image = img.read()
    crop_image = cv2.resize(bgr_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
    crop_image = bgr_image[0:SCREEN_HEIGHT, 0:SCREEN_WIDTH]
    capcap()
    
    if cv2.waitKey(1) & 0xFF == ord('q') :
            print ("interrupt!")
            




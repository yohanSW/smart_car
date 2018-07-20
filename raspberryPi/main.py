#*********************************libraries***************************************
import controlWheels
from time import sleep
import cv2
import cv2.cv as cv
import numpy as np
#*********************************************************************************

# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
show_image_enable   = False
draw_circle_enable  = True
scan_enable         = True
rear_wheels_enable  = True
front_wheels_enable = True
pan_enable          = True
adjusted_angle      = 0    # Calibrate the front wheel angle whose direction is straight
approach_angle		= 3

kernel = np.ones((5,5),np.uint8)

#####################openCv setting##############
img = cv2.VideoCapture(-1)  # choose a video

SCREEN_WIDTH = 640  # Screen width
SCREEN_HEIGHT = 480  # Screen Hight
img.set(3,SCREEN_WIDTH)
img.set(4,SCREEN_HEIGHT)

CENTER_X = SCREEN_WIDTH/2   #x coordinate of center of screen 
CENTER_Y = SCREEN_HEIGHT/2  #y coordinate of center of screen

# Camera setting
CAMERA_STEP = 2
CAMERA_X_ANGLE = 80
CAMERA_Y_ANGLE = 80
##################################################


cw = controlWheels.ControlWheels()
cw.offset = 0
cw.turn(adjusted_angle)

def nothing(x):
    pass

def main():
    global Stop
    print("Begin!")
	
    """
    make a thread code
    """
    while True:
        transition_angle = list()
        stopSignal = list()
        isNotFoundAngle = 0

        # image processing -> line trace , Determining whether to stop
        for i in range(9):
            transition_angle[i] , stopSignal[i] = image_processing()
            if transition_angle[i]==-700 :
                isNotFoundAngle += 1

        # stop state or If the road `isn't found
        if stopSignal > 4:
            print 'Stop signal!!!'
            cw.stop()
            continue
        elif isNotFoundAngle == 9:
            print 'Cannot detect line...'
            cw.stop()
            continue
        else :
            print 'Movement'
            angle = dataRefining(transition_angle)
            #straight move
            if angle < approach_angle and angle > -approach_angle :
                cw.turn_straight()
            #turning
            else:
                cw.turn(angle)

def destroy():
    return 0

def image_processing():
    return 30.5


def dataRefining(transition_angle):
    angle = 0
    angleCnt = 0
    angleRange = [0,0,0,0,0,0,0,0,0]
    angleRangeSub = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        angleRange[int(9[i]/10)] += 1
        angleRangeSub[int(transition_angle[i]/10)] += 1
        angleRange.sort()
        angleRange.reverse()
        meanRan = angleRangeSub.index(angleRange[0])
    for i in range(9):
        if transition_angle[i] >= meanRan*10 and transition_angle[i] < meanRan*10+10 :
            angle += transition_angle[i]
            angleCnt += 1
    return angle / angleCnt


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

        

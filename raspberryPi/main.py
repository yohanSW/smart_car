#*********************************libraries***************************************
import controlWheels
from time import sleep
from image_processing import image_processing
import numpy as np
import cv2
#*********************************************************************************
img = cv2.VideoCapture(0)
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
show_image_enable   = False
draw_circle_enable  = True
scan_enable         = True
rear_wheels_enable  = True
front_wheels_enable = True
pan_enable          = True
adjusted_angle      = 0    # Calibrate the front wheel angle whose direction is straight
approach_angle      = 3
error_signal        = -700
turning_max         = 40
image_cnt			= 7

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
        stopSignal = 0
        isNotFoundAngle = 0

        # image processing -> line trace , Determining whether to stop
        for i in range(image_cnt):
            angle_temp , stop_temp = image_processing(img)
            stopSignal += stop_temp
            if angle_temp == error_signal :
                isNotFoundAngle += 1
            elif angle_temp > turning_max :
                transition_angle.append(turning_max)
            elif angle_temp < -turning_max :
                transition_angle.append(-turning_max)
            else :
                transition_angle.append(angle_temp)

        # stop state or If the road `isn't found
        if stopSignal > (image_cnt/2) :
            #print 'Stop signal!!!'
            cw.stop()
            continue
        elif isNotFoundAngle == image_cnt:
            #print 'Cannot detect line...'
            cw.stop()
            continue
        else :
            #print 'Movement'
            angle = dataRefining(transition_angle, len(transition_angle))
            #straight move
            if angle < approach_angle and angle > -approach_angle :
                print("straight mode :")
                print (angle)
                cw.turn_straight()
            #turning
            else:
                print("turning mode : ")
                print(angle)
                cw.turn(angle)

def destroy():
    return 0

def dataRefining(transition_angle , cnt):
    angle = 0
    angleCnt = 0
    angleRange = [0,0,0,0,0,0,0,0,0]
    angleRangeSub = [0,0,0,0,0,0,0,0,0]
    for i in range(cnt):
        angleRange[int(transition_angle[i]/10)] += 1
        angleRangeSub[int(transition_angle[i]/10)] += 1
    angleRange.sort()
    angleRange.reverse()
    meanRan = angleRangeSub.index(angleRange[0])
    if meanRan > 4 :
        meanRan += -9
    for i in range(cnt):
        if transition_angle[i] >= meanRan*10 and transition_angle[i] < meanRan*10+10 :
            angle += transition_angle[i]
            angleCnt += 1
    if angle == 0 :
        return 0
    return angle / angleCnt


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

        

#*********************************libraries***************************************
from picar import controlWheels
from time import sleep
import cv2
import cv2.cv as cv
import numpy as np
import picar
#*********************************************************************************

picar.setup()
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
picar.setup()
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
		isFoundAngle = 0

		# image processing -> line trace , Determining whether to stop
		for i in range(9):
            transition_angle[i] = detectCentOfLine()
			isFoundAngle += transition_angle[i]
		for i in range(3):
			stopSignal += detectBreak()

		# stop state or If the road `isn't found
		if stopSignal > 2:
			print 'Stop signal!!!'
			cw.stop()
			continue
		elif isFoundAngle == 0:
			print 'Cannot detect line...'
			cw.stop()
			continue
        else :
			print 'Movement'
			angle = dataRefining(transition_angle)
			#straight move
			if angle < approach_angle && angle > -approach_angle :
				cw.turn_straight()
			#turning
			else
				cw.turn(angle)

def destroy():

def detectCentOfLine():

    '''
    INPUT : X
    OUTPUT : the (x, y) coordinate of center of road.
    REFERENCE : 
    '''
    # Load input image
    _, bgr_image = img.read()
    
    # Crop the image
    crop_image = bgr_image[60:240, 0:160]
    
    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
    
    # Set blue color range
    lower_blue = np.array([110, 50, 50])    
    upper_blue = np.array([130, 255, 255])

    '''
    # Set red color range
    lower_red = np.array([160, 20, 70])
    upper_red - np.array([190, 255, 255])
    '''

    #find the colors within the specified boundaries and apply
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        
        c = max(contours, key=cv2.contourArea)  #Choose the maximum area 
        M = cv2.moments(c)                      #Find center of the area

        # No exist contour, Use the center coordinate
        if M['m00'] == 0.0 :
            cx = CENTER_X
            cy = CENTER_Y
        
        else :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

        cv2.line(crop_image,(cx,0),(cx,720),(255,0,0),1)            #draw x-axis with blue line
        cv2.line(crop_image,(0,cy),(1280,cy),(255,0,0),1)           #draw y-axis with blue line
        cv2.drawContours(crop_image, contours, -1, (0,255,0), 1)    #draw contour with green line

    else:
        print "I can't detect the line"
        cx = 0
        cy = 0

    # Display the resulting frame
    cv2.imshow('frame',crop_image)
    cv2.imshow('mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        print "interrupt!"

    return cx, cy

def detectBreak():
	return 0;

def dataRefining(transition_angle):
	angle = 0
	angleCnt = 0
	angleRange = [0,0,0,0,0,0,0,0,0]
	angleRangeSub = [0,0,0,0,0,0,0,0,0]
	for i in range(9):
		angleRange[int(transition_angle[i]/10)] += 1
		angleRangeSub[int(transition_angle[i]/10)] += 1
	angleRange.sort()
	angleRange.reverse()
	meanRan = angleRangeSub.index(angleRange[0])
	for i in range(9):
		if transition_angle[i] >= meanRan*10 && transition_angle[i] < meanRan*10+10 :
			angle += transition_angle[i]
			angleCnt += 1
	return angle / angleCnt


if __name__ == '__main__':

    try:
        main()
        #find_face()
        #Red_lightsOn()

    except KeyboardInterrupt:
        destroy()

        
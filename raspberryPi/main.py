#*********************************libraries***************************************
from picar import front_wheels
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
adjusted_angle      = 75    # Calibrate the front wheel angle whose direction is straight

kernel = np.ones((5,5),np.uint8)

#####################openCv setting##############
img = cv2.VideoCapture(-1)  # choose a video

SCREEN_WIDTH = 160  # Screen width
SCREEN_HEIGHT = 120  # Screen Hight
img.set(3,SCREEN_WIDTH)
img.set(4,SCREEN_HEIGHT)

CENTER_X = SCREEN_WIDTH/2   #x coordinate of center of screen 
CENTER_Y = SCREEN_HEIGHT/2  #y coordinate of center of screen

# Camera setting
CAMERA_STEP = 2
CAMERA_X_ANGLE = 80
CAMERA_Y_ANGLE = 80
##################################################


fw = controlWheels.ControlWheels()
picar.setup()
fw.offset = 0
fw.turn(adjusted_angle)

def nothing(x):
    pass

def main():
	global Stop
	print("Begin!")
	scan_count = 0              # Count designated direction
	
	"""
	make a thread code

	"""
	while True:
		transition_angle = list()
		stopSignal = 0
		isFoundAngle = 0

		for i in range(9):
            transition_angle[i] = detectCentOfLine()
			isFoundAngle += transition_angle[i]

		for i in range(3):
			stopSignal += detectBreak()

		if stopSignal > 2 :

		# If the road `isn't found, isFound is False
        if isFoundAngle == 0 : 
            isFound = False
        else :
            isFound = True
            scan_count = 0

		#
		if isFound == False :
			print 'cannot detect line...'
			########### need more code########
		else :






def detectCentOfLine() :

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

def detectBreak() :
	return 0;

if __name__ == '__main__':

    try:
        main()
        #find_face()
        #Red_lightsOn()

    except KeyboardInterrupt:
        destroy()

        
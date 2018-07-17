#*********************************libraries***************************************
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
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

# Motor set
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 90
TILT_ANGLE_MIN  = 20
FW_ANGLE_MAX    = adjusted_angle+30
FW_ANGLE_MIN    = adjusted_angle-30

SCAN_POS = [50, 70, 90, 110, 130, 130, 110, 90, 70, 50] # range of sanning angle

# Front face detection data set
cascPath = '../../opencv/data/haarcascades/haarcascade_frontalface_alt.xml'

Stop = False    #global variable, if Stop is True, Car have to stop.
                #                 if Stop is False, Car have to go.

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(adjusted_angle)
pan_servo.write(90)
tilt_servo.write(60)
cx = 0 
cy = 0  

motor_speed = 45

def nothing(x):
    pass

def main():

    global Stop
    pan_angle = 90              # initial angle for pan
    tilt_angle = 60             # initial angle for tilt
    fw_angle = adjusted_angle   # initial angle for forward angle
  
    print("Begin!")
    scan_count = 0              # Count designated direction

    while True: 
    	x = 0             # x initial in the middle
        y = 0             # y initial in the middle
        
        # Find the center of contour
        for i in range(10):
            (x, y) = find_blob()
        
        # If the road isn't found, isFound is False
        if x == 0 and y == 0 : 
            isFound = False
        else :
            isFound = True
            scan_count = 0
            
        # Stop the car and Detect line
        if isFound == False :
            print 'scanning...'
            bw.stop()
            
            # Take the value of angle 
            if scan_enable:
                pan_angle = SCAN_POS[scan_count]
            
            # Move the pan-servo motor
            if pan_enable:
                pan_servo.write(pan_angle)
        
            scan_count += 1
        
            # Finish driving after scanning
            if scan_count >= len(SCAN_POS):
                
                print "End driving!"
                bw.stop()
                break
            
            else:
                sleep(0.1)     

        # Car follows the road
        else :
            '''
            The variation beteen CENTER of camera screen(CENTER_X, CENTER_Y) and the point which 
            means the CENTER of the road(x, y) decides how much the wheel have to move(delta_x, delta_y)
            '''
            delta_x = CENTER_X - x      
            delta_y = CENTER_Y - y

            print "x = %s, delta_x = %s" % (x, delta_x)
            print "y = %s, delta_y = %s" % (y, delta_y)
                
            # Degree for x-axis
            delta_angle = int(float(CAMERA_X_ANGLE) / SCREEN_WIDTH * delta_x) #Convert distance to angle
            print "delta_pan = %s" % delta_angle
            fw_angle = adjusted_angle - delta_angle #Calculate forward angle 
            
            # Front-wheel can move from FW_ANGLE_MIN to FW_ANGLE_MAX
            if fw_angle > FW_ANGLE_MAX:
                fw_angle = FW_ANGLE_MAX
            elif fw_angle < FW_ANGLE_MIN:
                fw_angle = FW_ANGLE_MIN
            
            # Normal range
            if FW_ANGLE_MIN < fw_angle and fw_angle < FW_ANGLE_MAX:

                # Turn forward wheel
                if front_wheels_enable:
                    fw.turn(fw_angle)
                
                # Move forward
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    bw.forward()

            # Out of range
            else:
                '''
                If fw_angle is over the range, they cannot move right way. So, they have to move back and  
                turn the wheel the opposite way. This algorithm makes car move right direction.
                '''
                bw.stop()
                fw_angle = (adjusted_angle - fw_angle) + adjusted_angle #Opposite direction of original way.
                
                # Turn the wheel the opposite side
                if front_wheels_enable:                
                    fw.turn(fw_angle)
                
                # Make backward speed down to protect (cx, cy) from being removed in the screen 
                if rear_wheels_enable:
                    bw.speed = motor_speed - 5
                    bw.backward()            

def destroy():
    '''
    INPUT : X
    OUTPUT : X
    REFERENCE : Makes car stop and end program.
    '''
    bw.stop()
    img.release()

def find_blob() :
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
    
def find_face() :
    '''
    INPUT : X
    OUTPUT : X 
    REFERENCE : Find front face 
    '''
    # Set up the route for front_face.xml
    faceCascade = cv2.CascadeClassifier(cascPath)

    if not faceCascade.load(cascPath) :
        print "--(!)Error loading\n"

    while True :
            
        # Load input image
        _, bgr_image = img.read()
        
        # Crop the image
        crop_image = bgr_image[60:240, 0:160]

        # Convert to grayscale
        gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.1,
                minNeighbors = 5,
                minSize = (30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )
            
        print "Found {0} faces!" .format(len(faces))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(crop_image, (x,y), (x+w, y+h), (0,255,0), 2)

        cv2.imshow('frame',crop_image)
        
        if cv2.waitKey(1) & 0xFF == ord('q') :
            print "interrupt!"

def Red_lightsOn() :
    '''
    INPUT : X
    OUTPUT : Red light returns True,
             Green light returns False 
    REFERENCE : Identify traffic light 
    '''
    global Stop

    lower_red = np.array([160, 20, 70])
    upper_red = np.array([190, 255, 255])

    lower_blue = np.array([110, 50, 50])    
    upper_blue = np.array([130, 255, 255])
    
    while True :
        # Load input image
        _, bgr_image = img.read()

        # Crop the image
        crop_image = bgr_image[60:240, 0:160]

        # Convert to HSV
        hsv = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)

        red_hue_range = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))

        # Use median filter to erase outlier(==noise)
        red_hue_image = cv2.medianBlur(red_hue_range, 5)

        # Use the Hough transform to detect circles in the combined threshold image
        circles = cv2.HoughCircles(red_hue_image, cv.CV_HOUGH_GRADIENT, 1, 120, 100, 20, 10, 0);

        # Loop over all detected circles and outline them on the original image        
        all_r = np.array([])

        if circles is not None:
            for i in circles[0]:
                all_r = np.append(all_r, int(round(i[2])))
            
            closest_ball        = all_r.argmax()
            center              = (int(round(circles[0][closest_ball][0])), int(round(circles[0][closest_ball][1])))
            radius              = int(round(circles[0][closest_ball][2]))
            
            # If red light is closed enough, then draw the circle
            if draw_circle_enable and radius > 5:
                cv2.circle(crop_image, center, radius, (0, 255, 0), 2);
                print "Stop!"
                Stop = True

        else : 
            # Capture the color range
            blue_hue_range = cv2.inRange(hsv, (110, 100, 100), (130, 255, 255))
            
            # Use median blur filter
            blue_hue_image = cv2.medianBlur(blue_hue_range, 5)

            # Use the Hough transform to detect circles in the combined threshold image
            circles = cv2.HoughCircles(blue_hue_image, cv.CV_HOUGH_GRADIENT, 1, 120, 100, 20, 10, 0);

            # Loop over all detected circles and outline them on the original image        
            if circles is not None:
                for i in circles[0]:
                    all_r = np.append(all_r, int(round(i[2])))
         
                closest_ball        = all_r.argmax()
                center              = (int(round(circles[0][closest_ball][0])), int(round(circles[0][closest_ball][1])))
                radius              = int(round(circles[0][closest_ball][2]))
                
                # If blue light is closed enough, then draw the circle
                if draw_circle_enable and radius > 5:
                    cv2.circle(crop_image, center, radius, (0, 255, 0), 2);
                    print "Go!"
                    Stop = False
        
        # Show image 
        cv2.imshow('frame', crop_image)


        if cv2.waitKey(1) & 0xFF == ord('q') :
            print "interrupt!"
    
if __name__ == '__main__':

    try:
        main()
        #find_face()
        #Red_lightsOn()

    except KeyboardInterrupt:
        destroy()

        

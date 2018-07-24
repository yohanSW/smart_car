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
#img = cv2.VideoCapture(0)
SCREEN_WIDTH = 640  # Screen Width
SCREEN_HEIGHT = 480  # Screen Height

def image_processing(img):
    # Load input image
    _, bgr_image = img.read()
    # Crop the image
    '''
        Example: bgr_image[height, width]
    '''
    #crop_image = bgr_image[0:1080, 0:1920]
    '''
        Parameters for default settings.
    '''
    LOWER_RADIUS = 20
    UPPER_RADIUS = 40
    stop_status_line = False
    stop_status_light = False
    draw_circle_enable = True
    crop_image = bgr_image[0:SCREEN_HEIGHT, 0:SCREEN_WIDTH]
    '''
        Epsilon will be used when dealing with "DIVISION by ZERO" error. Epsilon originally means "VERY SMALL number like 1e-6".
    '''
    eps = 1e-6

    #####################################<Traffic Light>##############################################
    '''
        ROI for detecting red light
    '''
    for_red_light = bgr_image[SCREEN_HEIGHT/3:480, 0:SCREEN_WIDTH].copy()
    #for_red_light = bgr_image[0:SCREEN_HEIGHT, 0:SCREEN_WIDTH].copy()
    
    '''
        1 frame of video(= 1 image) should go through filter to find red image.
        We will use HSV scheme for detecting red region
    '''
    hsv = cv2.cvtColor(for_red_light, cv2.COLOR_BGR2HSV)
    #originally, range of bgr value is (0,100,100) to (10, 255, 255)
    red_hue_image = cv2.inRange(hsv, (0,100,150), (10, 255, 255))
    red_hue_image = cv2.medianBlur(red_hue_image, 5)
    
    '''
        second parameters of houghcircles... you should change this code word.(Notice!)
        1) in raspberry pi -> cv2.cv.CV_HOUGH_GRADIENT
        2) in lattepanda -> cv2.HOUGH_GRADIENT
    '''
    circles = cv2.HoughCircles(red_hue_image, cv2.HOUGH_GRADIENT, 1, 120, 100, 20, 10, 0)
    
    '''
        List for putting all circles radius detected
    '''
    all_r = np.array([])
    try:
        if circles is not None:
            '''
                If circle(s) is(are) detected, then
                    A) append all radius to list named 'all_r'
                    B) save center position and radius
                    C) if the circle has radius which is above a threshold we set, then we will alert to the car.
            '''
            for i in circles[0]:
                all_r = np.append(all_r, int(round(i[2])))
            closest_ball = all_r.argmax()
            center=(int(round(circles[0][closest_ball][0])), int(round(circles[0][closest_ball][1] + SCREEN_HEIGHT/3)))
            radius = int(round(circles[0][closest_ball][2]))
            if draw_circle_enable and (radius >= LOWER_RADIUS and radius <= UPPER_RADIUS):
                cv2.circle(crop_image, center, radius, (0, 0, 255), 3)
                stop_status_light = True
        else:
            '''
                Doesn't have circles detected!
            '''
            stop_status_light = False
            #print("******no red light! go*******")
    except Exception as e:
        '''
            If you have some errors when you drives a car, then
                computer says that "There is no Red Light".
        '''
        stop_status_light = False
        #print("Error code when detecting circles... (No traffic light, go!!)->", e)
    #####################################################################################################

    '''
        About lane, we should use canny edge detection algorithm
    '''
    edge_image = cv2.Canny(crop_image, 150, 250, apertureSize=3)
    
    ########################<Stop Line>############################################################
    '''
        ROI for detecting stop line
    '''
    for_stop_line = edge_image[SCREEN_HEIGHT/2:SCREEN_HEIGHT, 0:SCREEN_WIDTH].copy()

    '''
        Detecting stop line using Hough-Transform
        This will return [[ [rho, theta], ... ]]
    '''
    lines_stop = cv2.HoughLines(for_stop_line, 1, np.pi/180, 30)
    sum_of_rho2 = 0
    sum_of_theta2 = 0
    try:
        '''
            We will use same logic as Lane detection
            1. get all lines (rho, theta)
            2. get sum and avg of rho and theta each.
            3. if we draw stop line, then just draw line using just average of rho and theta
            which is within some threshold angle
        '''
        if lines_stop is not None:
            for i in range(len(lines_stop[0])):
                sum_of_rho2 += lines_stop[0][i][0]
                sum_of_theta2 += lines_stop[0][i][1]
            avg_rho2 = sum_of_rho2 / len(lines_stop[0])
            avg_theta2 = sum_of_theta2 / len(lines_stop[0])
            # x * sin(avg_theta) + y * cos(avg_theta) = avg_rho
            if ((math.fabs(avg_theta2 * (180.0 / math.pi))) > 82 and math.fabs(avg_theta2 * (180.0 / math.pi)) < 98):
                #print("stop line. stop!!")
                cv2.line(crop_image, (int((avg_rho2-SCREEN_HEIGHT/2*math.sin(avg_theta2))/(math.cos(avg_theta2)+eps)),SCREEN_HEIGHT), (int(avg_rho2/math.cos(avg_theta2+eps)),SCREEN_HEIGHT/2),(0,0,255),10)      
                stop_status_line = True
            else:
                stop_status_line = False
        else:
            #print("no stop line. Go!")
            stop_status_line = False
    except Exception as e:
        stop_status_line = False
        #print("Error code when detecting stop lines... (No stop line, go!)->", e)
    #################################################################################################
    
    ########################<Lane Detection>############################################################
    '''
        Detecting lane using Hough-Transform
        This will return [[ [rho, theta], ... ]]
    '''
    lines = cv2.HoughLines(edge_image, 1, np.pi/180, 100)
    sum_of_rho = 0
    sum_of_theta = 0
    cnt = 0
    try:
        #print(lines)
        #print(lines[5][0][0])
        #print(lines[5][0][1])
        #(31, 1, 2)
        #[[[31, 24]], [[22, 44]], ...]
        if lines is not None:
            for i in range(len(lines[0])):
                sum_of_rho += lines[0][0][0]
                sum_of_theta += lines[0][0][1]
            '''
            while True:
                try:
                    sum_of_rho += lines[cnt][0][0]
                    sum_of_theta += lines[cnt][0][1]
                    cnt += 1
                except:
                    cnt -= 1
                    break
            avg_rho = sum_of_rho / float(cnt)
            avg_theta = sum_of_theta / float(cnt)
            '''
            avg_rho = sum_of_rho / len(lines[0])
            avg_theta = sum_of_theta / len(lines[0])
            angle = math.atan(float(SCREEN_HEIGHT)/(float(SCREEN_WIDTH/2) - (avg_rho)/math.cos(avg_theta))) * (180.0 / math.pi)
            if angle > 0:
                angle = 90 - angle
            else:
                angle = -(90 + angle)
            #print("Angle (left : pos, right : neg)-->", int(angle))
            '''
                Exception Handling : Early stop line detection -> just go forward!!
            '''
            if math.fabs(avg_theta * (180.0) / math.pi) > 72 and math.fabs(avg_theta * (180.0) / math.pi) < 108 and math.fabs(avg_rho) < (SCREEN_HEIGHT/2) and stop_status_line == False:
                cv2.line(crop_image, (320, 480), (320, 0), (255, 0, 255), 5)
                stop_status_line = False
                angle = 0.0
            else:
                cv2.line(crop_image, (int((avg_rho-SCREEN_HEIGHT*math.sin(avg_theta))/(math.cos(avg_theta)+eps)),SCREEN_HEIGHT), (int(avg_rho/math.cos(avg_theta+eps)),0),(255,0,0),3)
                cv2.line(crop_image, (SCREEN_WIDTH/2,SCREEN_HEIGHT), (int(avg_rho/math.cos(avg_theta+eps)),0),(0,255,0),3)
                if stop_status_line == True:
                    angle = 0.0
        else:
            #print("no lane. Stop!")
            angle = -700
    except Exception as e:
        #print(e)
        #print("no angle detected!!")
        #print("default error angle : 1000")
        angle = -700
    #################################################################################################
    if cv2.waitKey(1) & 0xFF == ord('q') :
        print ("interrupt!")
    #return angle, stop_status_line or stop_status_light
    cv2.imshow('Real World!',crop_image)
    #cv2.imshow('red', red_hue_image)
    return int(angle), stop_status_line or stop_status_light
'''
while True:
    #time.sleep(0.1)
    print(image_processing(img))
'''
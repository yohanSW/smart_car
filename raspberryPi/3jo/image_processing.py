'''
    Project : Autonomous Driving
    Developer : Song Chi Heon, Geum Dong Il

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
#img = cv2.VideoCapture(1)
#img = cv2.VideoCapture"/Users/chsong/Downloads/aabbcc/test1.mp4")
#cv2.useOptimized(True)
SCREEN_WIDTH = 320  # Screen Width
SCREEN_HEIGHT = 240  # Screen Height
CANNY_EDGE_LOWER = 130 # Canny Edge Lower Bound
CANNY_EDGE_UPPER = 250 # Canny Edge Upper Bound
HSV_RED_LOWER = (0,100,150)
HSV_RED_UPPER = (10,255,255)
LOWER_RADIUS = 20
UPPER_RADIUS = 40
gamma = 0.2
'''
    Epsilon will be used when dealing with "DIVISION by ZERO" error. Epsilon originally means "VERY SMALL number like 1e-6".
'''
eps = 1e-6

def adjust_gamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")
   return cv2.LUT(image, table)

def intensify_Contrast(original_image):
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize = (8,8))
    lab = cv2.cvtColor(original_image.copy(), cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)
    l2 = clahe.apply(l)
    lab = cv2.merge((l2,a,b))
    contrast_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return contrast_image

def getAngleFromLine(avg_rho, avg_theta):
    return math.atan(float(SCREEN_HEIGHT)/(float(SCREEN_WIDTH/2) - (avg_rho)/(math.cos(avg_theta)+eps))) * (180.0 / math.pi)

def find_Stop_Line(original_image, adjusted_image):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global CANNY_EDGE_LOWER
    global CANNY_EDGE_UPPER
    global eps
    '''
        About lane, we should use canny edge detection algorithm
    '''
    edge_image = cv2.Canny(adjusted_image, CANNY_EDGE_LOWER, CANNY_EDGE_UPPER, apertureSize=3)
    '''
        ROI for detecting stop line
    '''
    for_stop_line = edge_image[int((SCREEN_HEIGHT/2)):SCREEN_HEIGHT, 0:SCREEN_WIDTH].copy()

    '''
        Detecting stop line using Hough-Transform
        This will return [[ [rho, theta], ... ]]
    '''
    #originally, threshold is 30 at (1280 x 720)
    lines_stop = cv2.HoughLines(for_stop_line, 1, np.pi/180, 7)
    try:
        '''
            We will use same logic as Lane detection
            1. get all lines (rho, theta)
            2. get sum and avg of rho and theta each.
            3. if we draw stop line, then just draw line using just average of rho and theta
            which is within some threshold angle
        '''
        if lines_stop is not None:
            avg_rho = lines_stop[0][0][0]
            avg_theta = lines_stop[0][0][1]
            # x * sin(avg_theta) + y * cos(avg_theta) = avg_rho
            if ((math.fabs(avg_theta * (180.0 / math.pi))) > 82 and math.fabs(avg_theta * (180.0 / math.pi)) < 98):
                cv2.line(original_image, (int((avg_rho-SCREEN_HEIGHT/2*(math.sin(avg_theta)+eps)/(math.cos(avg_theta)+eps))),SCREEN_HEIGHT), (int(avg_rho/(math.cos(avg_theta)+eps)),SCREEN_HEIGHT/2),(0,0,255),10)
                return False, original_image
            else:
                return False, original_image
        else:
            return False, original_image
    except Exception as e:
        return False, original_image

def find_Lane(original_image, adjusted_image, is_Stop_at_StopLine):
    '''
        We will use same logic as Lane detection
        1. get all lines (rho, theta)
        2. get sum and avg of rho and theta each.
        3. if we draw stop line, then just draw line using just average of rho and theta
        which is within some threshold angle
    '''
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global CANNY_EDGE_LOWER
    global CANNY_EDGE_UPPER
    global eps
    edge_image = cv2.Canny(adjusted_image, CANNY_EDGE_LOWER, CANNY_EDGE_UPPER, apertureSize=3)
    edge_image_for_line = edge_image[int((SCREEN_HEIGHT/2)):SCREEN_HEIGHT, 0:SCREEN_WIDTH].copy()
    '''
        Detecting lane using Hough-Transform
        This will return [[ [rho, theta], ... ]]
    '''
    #originally, threshold is 100 at 1280x720
    lines = cv2.HoughLines(edge_image_for_line, 1, np.pi/180, 50)
    try:
        if lines is not None:
            avg_rho = lines[0][0][0]
            avg_theta = lines[0][0][1]
            angle = getAngleFromLine(avg_rho, avg_theta)
            if angle > 0:
                angle = 90 - angle
            else:
                angle = -(90 + angle)
            '''
                Exception Handling : Early stop line detection -> just go forward!!
            '''
            if math.fabs(avg_theta * (180.0) / math.pi) > 80 and math.fabs(avg_theta * (180.0) / math.pi) < 100 and math.fabs(avg_rho) < (SCREEN_HEIGHT/2) and is_Stop_at_StopLine == False:
                cv2.line(original_image, (SCREEN_WIDTH/2, SCREEN_HEIGHT), (SCREEN_WIDTH/2, 0), (255, 0, 255), 5)
                return 0.0, False, original_image
            else:
                cv2.line(original_image, (int((avg_rho-SCREEN_HEIGHT*math.sin(avg_theta))/(math.cos(avg_theta)+eps)),SCREEN_HEIGHT), (int(avg_rho/(math.cos(avg_theta)+eps)),0),(255,0,0),3)
                cv2.line(original_image, (SCREEN_WIDTH/2,SCREEN_HEIGHT), (int(avg_rho/(math.cos(avg_theta)+eps)),0),(0,255,0),3)
                if is_Stop_at_StopLine == True:
                    return 0.0, False, original_image
        else:
            return -700, False, original_image
    except Exception as e:
        return -700, False, original_image
    return angle, False, original_image

def find_Red_Traffic_Light(draw_circle_enable, original_image):
    global HSV_RED_LOWER
    global HSV_RED_UPPER
    global LOWER_RADIUS
    global UPPER_RADIUS
    stop_status_light = False
    '''
        ROI for detecting red light
    '''
    for_red_light = original_image[SCREEN_HEIGHT/3:int((SCREEN_HEIGHT/3)*2), 0:int(SCREEN_WIDTH/3)].copy()
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
            center = (int(round(circles[0][closest_ball][0])), int(round(circles[0][closest_ball][1] + SCREEN_HEIGHT/3)))
            radius = int(round(circles[0][closest_ball][2]))
            if draw_circle_enable and (radius >= LOWER_RADIUS and radius <= UPPER_RADIUS):
                cv2.circle(original_image, center, radius, (0, 0, 255), 3)
                stop_status_light = True
        else:
            return False, original_image
    except Exception as e:
        return False, original_image
    return stop_status_light, original_image

def image_processing(img):
    # Load input image
    global gamma
    _, bgr_image = img.read()
    stop_status_line = False
    stop_status_light = False
    draw_circle_enable = False

    '''
        Adjust noisy image
    '''
    #original_image = cv2.resize(bgr_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
    original_image = bgr_image[0:SCREEN_HEIGHT, 0:SCREEN_WIDTH]
    adjusted_contrast = intensify_Contrast(original_image)
    gamma_correction = adjust_gamma(adjusted_contrast, gamma=gamma)

    '''
        Detecting red light, stop line and lane
    '''
    stop_status_light, original_image = find_Red_Traffic_Light(draw_circle_enable, original_image)
    stop_status_line, original_image = find_Stop_Line(original_image, gamma_correction)
    angle, stop_status_line, original_image = find_Lane(original_image, gamma_correction, stop_status_line)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        print ("interrupt!")
    cv2.imshow('Real World!',original_image)
    cv2.imshow('gamma',gamma_correction)
    return int(angle), stop_status_line or stop_status_light

'''
while True:
    #time.sleep(0.1)
    print(image_processing(img))
'''
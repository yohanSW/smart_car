import serial 
import RPi.GPIO as GPIO
import time
import sense
import gps_detect
import subprocess
GPIO.setmode(GPIO.BOARD)
pin = 11 #LED pin 
NoTouchStack = 0
geo_count = 0
GPIO.setup(pin,GPIO.OUT)



def new_tech():
    sense.GoSignal()
    impact, fire, sona, heartpulse, touchresult  = sense.sensing()
    '''if fire == -1 :
        continue'''
    try:
        global NoTouchStack
        global com_alarm
        global geo_count
        com_alarm = "''"
        Accident = 0
        
        """
        if  (heartpulse <=180 and heartpulse >= 130) : ##normal heartpulse is between 49 ~ 90
            com_alarm = "'Driver is under heart attack'"
            print(com_alarm)
            #if heart attack has been happend, Auto driving must be started!!
            sense.ClutchControl()
            sense.ClutchAlarm()
            #GPIO.output(ClutchControl,True) ##Auto Driving start
            #GPIO.output(ClutchAlarm,True) ##Alarm to Arduino that Clutch is on signal
            Accident = 1
        """
        if fire <= 400 : ##fire signal is measured as analog, if it is over 500, then there are fire around sensor.
            com_alarm = "'Fire Fire Fire'"
            print(com_alarm)
            sense.BrakeControl()
            #GPIO.output(BrakeControl,True) ##if the car is on fire, car must be stopped
            Accident = 2
        if impact >= 400 and ( sona <= 10 or sona >= 4000 ) : ##sona data occasionally measured as 2000~2500 without any reason.
            com_alarm = "'Car crush has been happened'"
            print(com_alarm)
            Accident = 3
            if touchresult == 0 :
                NoTouchStack = NoTouchStack + 1
            if NoTouchStack == 2 :
                #sense.ClutchControl()
                sense.ClutchAlarm()
                #GPIO.output(ClutchControl,True) ##Auto Driving start
                #GPIO.output(ClutchAlarm,True) ##Alarm to Arduino that Clutch is on signal
                print("Driver can't handle the car. Start the Auto Driving Mode")
                Accident = 4
                NoTouchStack = 0
            else :
                NoTouchStack = 0
            ###########################################################################################################        
        if Accident > 0 : # if Accident happend,
            sense.WaitSignal()
            led_sos()
            ##gpsx, gpsy = gps() # GPS signal is transmitted
            str_com_1 = "sudo systemctl stop gpsd.socket"
            str_com_2 = "sudo systemctl disable gpsd.socket"
            str_com_3 = "sudo systemctl enable gpsd.socket"
            str_com_4 = "sudo systemctl start gpsd.socket"
            str_com_5 = "sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock"
            subprocess.check_output(str_com_1,shell=True)
            subprocess.check_output(str_com_2,shell=True)
            subprocess.check_output(str_com_3,shell=True)
            subprocess.check_output(str_com_4,shell=True)
            subprocess.check_output(str_com_5,shell=True)
            print("GPS detection started")
            if geo_count == 0 : 
                #gps_detect()
                str_com_6 = "sudo python3 gps_detect.py"
                subprocess.check_output(str_com_6,shell=True)
                print("GPS detection finished and Map was downloaded on the folder")
                ##upload twitter
                ####make code here!
                geo_count += 1
            else :
                print("GPS is already once detected, so no longer we print gps...")
                
            print("Image is uploaded on twit")
            str_com ="python3 post_image.py high_resolution_image.png " + com_alarm
            subprocess.check_output(str_com,shell=True)
            print("Image upload is finished")
        else :
            sense.AllNormal()
            #GPIO.output(ClutchControl,False) ##if there is no accident, clutch is off
            #GPIO.output(ClutchAlarm,False)
            #GPIO.output(BrakeControl,False) ##if there is no accident, brake is off
    except Exception as e:
        print(e)
        #GPIO.cleanup()
        #break

def destroy():
    return 0

def led_sos():
######################LED SOS SIGNAL######################
    for i in range(1) : # SOS 3 times
        for i in range(3) : # signal 'S'
            GPIO.output(pin,True)
            time.sleep(0.3)
            GPIO.output(pin,False)
            time.sleep(0.25)
        time.sleep(0.3)
        for i in range(3) : # signal 'O'
            GPIO.output(pin,True)
            time.sleep(0.8)
            GPIO.output(pin,False)
            time.sleep(0.25)
        time.sleep(0.3)
        for i in range(3) : # signal 'S'
            GPIO.output(pin,True)
            time.sleep(0.3)
            GPIO.output(pin,False)
            time.sleep(0.25)
        time.sleep(1)



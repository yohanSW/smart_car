import serial
import RPi.GPIO as GPIO
import time
import sense

GPIO.setmode(GPIO.BOARD)
pin = 11 #LED pin 
BrakeControl = 13 #Brake control pin number ( In Arduino , pin 10 )
ClutchAlarm = 15 #Clutch Alarm to Arduino ( In Arduino, pin 9 )
ClutchControl = 16 #Clutch control pin number
NoTouchStack = 0
auto_driving_switch = 18 #auto_driving_switch
new_tech_switch = 22 #new_tech_switch
#ser = serial.Serial("/dev/ttyACM0",115200)
GPIO.setup(pin,GPIO.OUT)
GPIO.setup(BrakeControl,GPIO.OUT)
GPIO.setup(ClutchAlarm,GPIO.OUT)
GPIO.setup(auto_driving_switch , GPIO.IN)
GPIO.setup(new_tech_switch , GPIO.IN)

def main():
    print "main code start!"
    while True :
        if GPIO.input(auto_driving_switch)==1:
            GPIO.output(ClutchControl,True) ##Auto Driving start
            GPIO.output(ClutchAlarm,True) ##Alarm to Arduino that Clutch is on signal
            GPIO.output(BrakeControl,False) ##if the car is on fire, car must be stopped
        elif GPIO.input(new_tech_switch)==1:
            new_tech()
        else
            GPIO.output(ClutchControl,False) ##Auto Driving start
            GPIO.output(ClutchAlarm,False) ##Alarm to Arduino that Clutch is on signal
            GPIO.output(BrakeControl,False) ##if the car is on fire, car must be stopped




def new_tech():
    while True : 
        impact, fire, sona, heartpulse, touchresult  = sense.sensing()
        '''if fire == -1 :
            continue'''
        try:
            while True :
    
                Accident = 0
                
                if  (heartpulse <=180 and heartpulse >= 130) or heartpulse <=30 : ##normal heartpulse is between 49 ~ 90
                    print("Driver is under heart attack")
                    #if heart attack has been happend, Auto driving must be started!!
                    GPIO.output(ClutchControl,True) ##Auto Driving start
                    GPIO.output(ClutchAlarm,True) ##Alarm to Arduino that Clutch is on signal
                    Accident = 1
                if fire >= 600 : ##fire signal is measured as analog, if it is over 500, then there are fire around sensor.
                    print("Fire Fire Fire")
                    GPIO.output(BrakeControl,True) ##if the car is on fire, car must be stopped
                    Accident = 1
                if impact >= 400 and ( sona <= 10 or sona >= 4000 ) : ##sona data occasionally measured as 2000~2500 without any reason.
                    print("Car crush has been happened")
                    Accident = 1

                if touchresult == 0 :
                    NoTouchStack = NoTouchStack + 1
                    if NoTouchStack == 3 :
                        GPIO.output(ClutchControl,True) ##Auto Driving start
                        GPIO.output(ClutchAlarm,True) ##Alarm to Arduino that Clutch is on signal
                        print("Driver can't handle the car. Start the Auto Driving Mode")
                        NoTouchStack = 0
                else
                    NoTouchStack = 0


                ###########################################################################################################        
                if Accident == 1 : # if Accident happend,
                    sense.WaitSignal()
                    ##gpsx, gpsy = gps() # GPS signal is transmitted
                    ####make code here!
                    ##upload twitter
                    ####make code here!
                    led_sos()
                    break
                else:
                    GPIO.output(ClutchControl,False) ##if there is no accident, clutch is off
                    GPIO.output(ClutchAlarm,False)
                    GPIO.output(BrakeControl,False) ##if there is no accident, brake is off
                    break
        except Exception as e:
            print(e)
            GPIO.cleanup()
            break
    
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

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

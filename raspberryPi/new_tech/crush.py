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
#ser = serial.Serial("/dev/ttyACM0",115200)
GPIO.setup(pin,GPIO.OUT)
GPIO.setup(BrakeControl,GPIO.OUT)
GPIO.setup(ClutchAlarm,GPIO.OUT)


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
                
            if touchresult = 0 :
                NoTouchStack = NoTouchStack + 1
                if NoTouchStack == 3 :
                    GPIO.output(ClutchControl,True) ##Auto Driving start
                    GPIO.output(ClutchAlarm,True) ##Alarm to Arduino that Clutch is on signal
                    print("Driver can't handle the car. Start the Auto Driving Mode")
                    NoTouchStack = 0
            else
                NoTouchStack = 0
                    
            
            


            if Accident == 1 : # if Accident happend,
                
                sense.WaitSignal()
                
                ##gpsx, gpsy = gps() # GPS signal is transmitted,
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
                #GPIO.cleanup()
                break
            else:
                GPIO.output(ClutchControl,False) ##if there is no accident, clutch is off
                GPIO.output(ClutchAlarm,False)
                GPIO.output(BrakeControl,False) ##if there is no accident, brake is off
                break
    except Exception as e:
        print(e)
        break



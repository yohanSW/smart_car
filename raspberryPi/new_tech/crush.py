import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
pin = 11

def crush():
    #set var

    while True :
        while True :

            Accident = 0 

            if fire == 1 :
                print("Fire Fire Fire")
                Accident = 1

            if heartpulse >= 130 and heartpulse <=40 :
                print("Driver is under heart attack")
                #if heart attack has been happend, Auto driving must be started!!
                Accident = 1

            if impact == 1 and ( sona <= 40 or sona >= 1000 ) :
                print("Car crush has been happened")
                Accident = 1
        
        
            if Accident == 1 : # if Accident happend,

                gpsx, gpsy = gps() # GPS signal is transmitted,

                for i in range(5) : # led blinked 5 times.
                    GPIO.output(pin,True)
                    time.sleep(1)
                    GPIO.output(pin,False)
                    time.sleep(1)
                GPIO.cleanup()
                break


def sensing():

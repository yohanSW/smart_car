import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
pin = 11 #LED pin number

def crush():
    #set var
	if ((fd = serialOpen ("/dev/ttyACM0", 115200)) < 0)  // 두번째 인자값이 보레이트 설정

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

                ######################LED SOS SIGNAL######################
                for i in range(3) : # SOS 3 times
                    for i in range(3) : # signal 'S'
                        GPIO.output(pin,True)
                        time.sleep(0.5)
                        GPIO.output(pin,False)
                        time.sleep(1)
                    for i in range(3) : # signal 'O'
                        GPIO.output(pin,True)
                        time.sleep(3)
                        GPIO.output(pin,False)
                        time.sleep(1)    
                    for i in range(3) : # signal 'S'
                        GPIO.output(pin,True)
                        time.sleep(0.5)
                        GPIO.output(pin,False)
                        time.sleep(1)

                GPIO.cleanup()
                break


def sensing():
	return fire , heartpulse , sona , impact


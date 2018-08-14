import RPi.GPIO as GPIO
import time
import sense
import crush
GPIO.setmode(GPIO.BOARD)
auto_driving_switch = 18 #auto_driving_switch
new_tech_switch = 22 #new_tech_switch
GPIO.setup(auto_driving_switch , GPIO.IN)
GPIO.setup(new_tech_switch , GPIO.IN)

def main():
    print ("main code start!")
    #new_tech()
    while True :
        judgeNum = sense.judge()
        if judgeNum == 1:
            if GPIO.input(auto_driving_switch)==1:
                sense.ClutchAlarm()
            elif GPIO.input(new_tech_switch)==1:
                crush.new_tech()
            else :
                sense.AllNormal()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()


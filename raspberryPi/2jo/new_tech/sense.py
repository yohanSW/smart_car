import serial

ser = serial.Serial("/dev/ttyACM0",115200)
def WaitSignal():
    #ser.write(str.encode('W')) #W is Wait
    ser.write(str.encode('#5')
    print("SOS Signal Activated")

def BrakeControl():
    #ser.write(str.encode('B')) #B is Brake
    ser.write(str.encode('#4')
    print("Brake Brake Brake")

"""
    def ClutchControl():
    ser.write(str.encode('C')) #C is Clutch control
    print("Auto driving is started")
"""

def ClutchAlarm():
    #ser.write(str.encode('A')) #A is clutch Alarm
    ser.write(str.encode('#2')
    print("Clutch signal is transmitted to Motor Control Arduino")

def AllNormal():
    #ser.write(str.encode('N')) #N is Normal
    ser.write(str.encode('#3')
    print("All state is normal, manual driving is started again")
    
def GoSignal():
    #ser.write(str.encode('G'))
    ser.write(str.encode('#1'))

def sensing():
    ##print('c')
    if ser.readable() :
        impact = int(ser.readline())
        fire = int(ser.readline())
        sona = int(ser.readline())
        heartpulse = int(ser.readline())
        touchresult = int(ser.readline())
        print("impact : " + str(impact))
        print("fire : " + str(fire))
        print("sona : " + str(sona))
        print("heartpulse : " + str(heartpulse))
        print("touchresult : " + str(touchresult))
    else :
        return -1, -1, -1, -1, -1
    return impact, fire, sona, heartpulse, touchresult

def judge():
    global Gosignal
    if ser.inWaiting()>0 :
        Gosignal = ser.readline()
        print("sig: ", Gosignal)
        if Gosignal == 'G\r\n' :
            print("aaa")
            return 1
        else:
            return 0
    else:
        return 0



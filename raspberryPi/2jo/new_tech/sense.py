import serial

ser = serial.Serial("/dev/ttyACM0",115200)
def WaitSignal():
    ser.write(str.encode('W')) #W is Wait
    print("SOS Signal Activated")

def BrakeControl():
    ser.write(str.encode('B')) #B is Brake
    print("Brake Brake Brake")

def ClutchControl():
    ser.write(str.encode('C')) #C is Clutch control
    print("Auto driving is started")

def ClutchAlarm():
    ser.write(str.encode('A')) #A is clutch Alarm
    print("Clutch signal is transmitted to Motor Control Arduino")

def AllNormal():
    ser.write(str.encode('N')) #N is Normal
    print("All state is normal, manual driving is started again")
    
def GoSignal():
    ser.write(str.encode('G'))

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




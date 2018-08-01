import serial

ser = serial.Serial("/dev/ttyACM0",115200)

def WaitSignal():
    WaitSignal = 1
    ser.write(str(WaitSignal))
    print("SOS Signal Activated")

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



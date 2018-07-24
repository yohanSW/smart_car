#!/usr/bin/env python
#################
import filedb
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
print "wowowo"

class ControlWheels(object):
    ''' Front wheels control class '''
    def __init__(self, debug=False, db="config"):
        ''' setup channels and basic stuff '''
        self.db = filedb.fileDB(db=db)
        self._straight_angle = 0
        self.turning_max = 40
        self._min_angle = -self.turning_max
        self._max_angle = self.turning_max
        self._turning_offset = int(self.db.get('turning_offset', default_value=0))
        self._angle = {"left":self._min_angle, "straight":self._straight_angle, "right":self._max_angle}
        self._nowAngle = self._straight_angle

    def turn_straight(self):
        ''' Turn the front wheels back straight '''
        self.arduino(self._angle["straight"], 0)

    def turn(self, angle):
        ''' Turn the front wheels to the giving angle '''
        print("turning angle : ")
        print(angle)
        if angle < self._angle["left"]:
            angle = self._angle["left"]
        if angle > self._angle["right"]:
            angle = self._angle["right"]
        self._nowAngle = angle
        self.arduino(angle, 0)

    def stop(self):
        ''' Stop both wheels '''
        ########need make motor control code
        self.arduino(self._nowAngle, 1)

    def arduino(self,angle,stopSig):
        minus_sig = 1
        if(angle < 0):
            angle = -angle
            minus_sig = 0
		ser_str = '#'+ str(minus_sig) + ' , ' + str(int(angle)) +' , ' + str(stopSig)
        ser.write(ser_str)
		print("wow")


'''
def test(chn=0):
    import time
    controlWheels = ControlWheels()
    try:
        while True:
            print "turn_straight"
            controlWheels.turn_straight()
            time.sleep(1)
            print "turn_right"
            controlWheels.turn(30)
            time.sleep(1)
            print "turn_left"
            controlWheels.turn(-20)
            time.sleep(1)
            print "stop"
            controlWheels.stop()
    except KeyboardInterrupt:
        controlWheels.turn_straight()

if __name__ == '__main__':
    test()
'''




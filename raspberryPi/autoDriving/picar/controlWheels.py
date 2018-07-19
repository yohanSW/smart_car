#!/usr/bin/env python

from SunFounder_PCA9685 import Servo
import filedb
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
cnt = 0

class ControlWheels(object):
	''' Front wheels control class '''

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "controlWheels.py":'

	def __init__(self, debug=False, db="config"):
		''' setup channels and basic stuff '''
		self.db = filedb.fileDB(db=db)
		self._straight_angle = 0
		self.turning_max = 35
		self._min_angle = -self.turning_max
		self._max_angle = self.turning_max
		self._turning_offset = int(self.db.get('turning_offset', default_value=0))
		self._angle = {"left":self._min_angle, "straight":self._straight_angle, "right":self._max_angle}
		self._nowAngle = self._straight_angle

	def turn_straight(self):
		''' Turn the front wheels back straight '''
		self.arduino(self._angle["straight"], False)

	def turn(self, angle):
		''' Turn the front wheels to the giving angle '''
		if angle < self._angle["left"]:
			angle = self._angle["left"]
		if angle > self._angle["right"]:
			angle = self._angle["right"]
		self._nowAngle = angle
		self.arduino(angle, False)

	def stop(self):
		''' Stop both wheels '''
		########need make motor control code
		if self._DEBUG:
			print self._DEBUG_INFO, 'Stop'
		self.arduino(self._nowAngle, True)
		
	def arduino(self,angle,stopSig)
		cnt += 1
		ser.write('#' + str(cnt) ,'!' + str(angle), '@' + str(stopSig))



def test(chn=0):
	import time
	controlWheels = ControlWheels(channel=chn)
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




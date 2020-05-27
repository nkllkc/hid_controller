import json
from configs import *
import time
import threading
#from filelock import Timeout, FileLock

def loadMappings(mappingFile = 'keycodes.json', shiftOnFile = 'shift_on.nfo'):
	with open(mappingFile) as json_file:
		mappings = json.load(json_file)

	with open(shiftOnFile) as set_file:
		shiftOn = set(set_file.read().split(" "))
		shiftOn.remove('')

	return mappings, shiftOn

hidFile = '/dev/hidg0';
#hidFile = 'hid';
#lockFile = '/dev/hidg0.lock';
#lock = FileLock(lockFile);

def write_report(report):
	with open(hidFile, 'rb+') as fd:
		fd.write(report.encode())
		fd.flush()

class EventProcessor:

	def __init__(self, mappings, shiftOn, logging, calibrate = True, hidFile = '/dev/hidg0'):
		self.mappings = mappings
		self.shiftOn = shiftOn
		self.logging = logging
		self.hidFile = hidFile
		self.lock = threading.Lock()
		if calibrate:
			self.calibratePointer()
		#super().__init__()

	def write_report(self, report):
		with open(self.hidFile, 'rb+') as fd:
			fd.write(report.encode())
	# Move the pointer to upper-left corner.
	def calibratePointer(self):
		self.currentX = 0
		self.currentY = 0

		self.logging.debug("Calibrating!")
		# TODO: Make this move diagonal.
		for i in range (0, WIDTH):
			write_report(LEFT_STEP_REPORT)
		for i in range (0, HEIGHT):
			write_report(UP_STEP_REPORT)

	def createReportFromKey(self, key):
		if key.islower():
			string = NULL_CHAR * 2 + chr(self.mappings[key]) + NULL_CHAR * 5 + NULL_REPORT*8
		elif key.isupper():
			string = SHIFT_CHAR + NULL_CHAR + chr(self.mappings[key.lower()]) + NULL_CHAR * 5 + NULL_REPORT*8
		else:
			if key not in self.mappings:
				self.logging.debug("Missing key: %s!", key)
				return
			if key in self.shiftOn:
				string = chr(32) + NULL_CHAR + chr(self.mappings[key]) + NULL_CHAR * 5 + NULL_REPORT*8
			else:
				string = NULL_CHAR * 2 + chr(self.mappings[key]) + NULL_CHAR * 5 + NULL_REPORT*8
		return string

	def execute_keyboard_command(self, key):
		self.logging.debug("Pressed key: %s", key)
		string = self.createReportFromKey(key)
		write_report(string)


	def executeMouseCommand(self, xPercentage, yPercentage, click):
		self.lock.acquire()
		self.logging.debug("Exec mouse cmd: %.3f, %.3f, %s", xPercentage, yPercentage, click)
		newX = int(round(xPercentage * WIDTH))
		newY = int(round(yPercentage * HEIGHT))

		self.logging.debug("new x: %d", newX)
		self.logging.debug("newy: %d", newY)

		diffX = int(abs(newX - self.currentX))
		diffY = int(abs(newY - self.currentY))
		
		self.logging.debug("diffX: %d", diffX)
		self.logging.debug("diffY: %d", diffY)

		xMove = RIGHT_STEP_REPORT
		if newX <= self.currentX:
			xMove = LEFT_STEP_REPORT

		yMove = DOWN_STEP_REPORT
		if newY <= self.currentY:
			yMove = UP_STEP_REPORT

		for i in range(0, diffX):
			write_report(xMove)

		for i in range(0, diffY):
			write_report(yMove)
				
		
		
		#write_report(TOUCH_REPORT)
		if(click):
			write_report(PRESS_REPORT)
		#time.sleep(0.1)
		else:
			time.sleep(0.05)
			write_report(RELEASE_REPORT)
		#write_report(DOUBLE_TOUCH)
		#write_report(PRESS_RELEASE_REPORT)
		self.currentY = newY
		self.currentX = newX
		self.lock.release()





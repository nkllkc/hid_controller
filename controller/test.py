import socketio
import logging
import struct
import string
import json

import fileinput

# Set the appropriate log level.
logging.basicConfig(level=logging.DEBUG)

class Event:
    def __init__(self, data):
            self.__dict__ = json.loads(data)

NULL_CHAR = chr(0)
NULL_REPORT = NULL_CHAR * 8

# TODO: Make this configurable.
WIDTH = 48
HEIGHT = 86

RIGHT_ARROW = 79
LEFT_ARROW = 80
DOWN_ARROW = 81
UP_ARROW = 82

RIGHT_STEP = NULL_CHAR * 2 + chr(RIGHT_ARROW) + NULL_CHAR * 5 + NULL_REPORT
LEFT_STEP = NULL_CHAR * 2 + chr(LEFT_ARROW) + NULL_CHAR * 5 + NULL_REPORT
DOWN_STEP = NULL_CHAR * 2 + chr(DOWN_ARROW) + NULL_CHAR * 5 + NULL_REPORT
UP_STEP = NULL_CHAR * 2 + chr(UP_ARROW) + NULL_CHAR * 5  + NULL_REPORT

shift_on = set()
mappings = {}

currentX = 0
currentY = 0


def write_report(report):
	with open('/dev/hidg0', 'rb+') as fd:
		fd.write(report.encode())	

# Move the pointer to upper-left corner.
def calibrate_pointer():
	global currentX
	global currentY

	currentX = 0
	currentY = 0

	for i in range (0, WIDTH):
		write_report(LEFT_STEP)
	for i in range (0, HEIGHT):
		write_report(UP_STEP)	


def execute_keyboard_command(key):
	logging.debug("USING %s", key)
	if key.islower():
		string = NULL_CHAR * 2 + chr(mappings[key]) + NULL_CHAR * 5
	elif key.isupper():
		string = chr(32) + NULL_CHAR + chr(mappings[key.lower()]) + NULL_CHAR * 5
	else:
		if key not in mappings:
			logging.debug("Missing key: %s!", key)
			return
		if key in shift_on:
			string = chr(32) + NULL_CHAR + chr(mappings[key]) + NULL_CHAR * 5
		else:
			string = NULL_CHAR * 2 + chr(mappings[key]) + NULL_CHAR * 5
	write_report(string, True)


def execute_mouse_command(xPercentage, yPercentage):
	global currentX
	global currentY
	
	newX = int(round(xPercentage * WIDTH))
	newY = int(round(yPercentage * HEIGHT))

	diffX = int(abs(newX - currentX))
	diffY = int(abs(newY - currentY))

	xMove = RIGHT_STEP
	if newX <= currentX:
		xMove = LEFT_STEP
	
	yMove = DOWN_STEP
	if newY <= currentY:
		yMove = UP_STEP
	
	for i in range(0, diffX):
		write_report(xMove)

	for i in range(0, diffY):
		write_report(yMove)
	
	currentY = newY
	currentX = newX

if __name__== "__main__":
	
	calibrate_pointer()

	for line in fileinput.input():
		try:
			args = line.split(' ')
			x = float(args[0])
			y = float(args[1])
			execute_mouse_command(x, y)
		except:
			break
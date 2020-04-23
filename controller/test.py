import socketio
import logging
import struct
import string
import json

import fileinput

from sys import argv

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

# Keypads 6, 4, 2, 8.
# 
# Here yu can find more about how this works: 
# https://support.apple.com/guide/mac-help/control-the-pointer-using-mouse-keys-mh27469/mac
RIGHT_ARROW = 94
LEFT_ARROW = 92
DOWN_ARROW = 90
UP_ARROW = 96
TOUCH = 93 # Keypad 5.
PRESS = 98 # Keypad 0.
RELEASE = 99 # Keypad .(dot).

RIGHT_STEP_REPORT = NULL_CHAR * 2 + chr(RIGHT_ARROW) + NULL_CHAR * 5 + NULL_REPORT
LEFT_STEP_REPORT = NULL_CHAR * 2 + chr(LEFT_ARROW) + NULL_CHAR * 5 + NULL_REPORT
DOWN_STEP_REPORT = NULL_CHAR * 2 + chr(DOWN_ARROW) + NULL_CHAR * 5 + NULL_REPORT
UP_STEP_REPORT = NULL_CHAR * 2 + chr(UP_ARROW) + NULL_CHAR * 5  + NULL_REPORT
TOUCH_REPORT = NULL_CHAR * 2 + chr(TOUCH) + NULL_CHAR * 5  + NULL_REPORT
PRESS_REPORT = NULL_CHAR * 2 + chr(PRESS) + NULL_CHAR * 5  + NULL_REPORT
RELEASE_REPORT = NULL_CHAR * 2 + chr(RELEASE) + NULL_CHAR * 5  + NULL_REPORT

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
		write_report(LEFT_STEP_REPORT)
	for i in range (0, HEIGHT):
		write_report(UP_STEP_REPORT)	


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


def execute_mouse_command(xPercentage, yPercentage, click):
	print("execute_mouse_command")

	global currentX
	global currentY
	
	newX = int(round(xPercentage * WIDTH))
	newY = int(round(yPercentage * HEIGHT))

	diffX = int(abs(newX - currentX))
	diffY = int(abs(newY - currentY))

	xMove = RIGHT_STEP_REPORT
	if newX <= currentX:
		xMove = LEFT_STEP_REPORT
	
	yMove = DOWN_STEP_REPORT
	if newY <= currentY:
		yMove = UP_STEP_REPORT
	
	for i in range(0, diffX):
		write_report(xMove)

	for i in range(0, diffY):
		write_report(yMove)

	if click:
		print("CLICKED")
		write_report(TOUCH_REPORT)

	
	currentY = newY
	currentX = newX

if __name__== "__main__":
	
	calibrate_pointer()

	for line in fileinput.input():
		try:
			args = line.split(' ')
			print(args)
			x = float(args[0])
			y = float(args[1])
			print(x)
			print(y)
			print(args[2][0] == 'y')
			execute_mouse_command(x, y, args[2][0] == 'y')
		except:
			break

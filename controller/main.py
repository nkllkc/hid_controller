import socketio
import logging
import struct
import string
import json

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


def write_report(report):
	with open('/dev/hidg0', 'rb+') as fd:
		fd.write(report.encode())


def execute_keyboard_command(key):
	logging.debug("USING %s", key)
	if key.islower():
		string = NULL_CHAR * 2 + chr(mappings[key]) + NULL_CHAR * 5
	elif key.isupper():
		string = chr(32) + NULL_CHAR + chr(mappings[key.lower()]) + NULL_CHAR * 5
	else:
#		key = key.lower()
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
	
	actualX = int(round(xPercentage * WIDTH))
	actualY = int(round(yPercentage * HEIGHT))

	diffX = int(abs(actualX - currentX))
	diffY = int(abs(actualY - currentY))

	xMove = RIGHT_STEP
	if actualX <= currentX:
		xMove = LEFT_STEP
	
	yMove = DOWN_STEP
	if actualY <= currentY:
		yMove = UP_STEP
	
	for i in range(0, diffX):
		write_report(xMove)

	for i in range(0, diffY):
		write_report(yMove)
	
	currentY = actualY
	currentX = actualX

sio = socketio.Client()

@sio.event
def connect():
	logging.info('Connection established!')
	execute_mouse_command(0, 0)
	logging.info('Moving the pointer to the 0, 0!')

@sio.event
def disconnect():
	logging.error('Disconnected from the GCP GAE.')

# event_console2server
@sio.on('event_server2client')
def event_server2client(data):
	event = Event(data)

	if event.type != 'mouse_click':
		logging.error("WRONG CALLBACK! Non mouse_click in event_server2client")
		return
	
	logging.debug(data)
	logging.debug("Event.Type: -%s-", event.type)
	
	execute_mouse_command(event.xPercentage, event.xPercentage)

@sio.on('event_server2client_keyboard')
def event_server2client_keyboard(data):
	event = Event(data)

	if event.type == 'mouse_click':
		logging.error("WRONG CALLBACK! mouse_click in event_server2client_keyboard")
		return

	logging.debug(data)
	logging.debug("key: -%s-", event.type)


def init_maps():
	global mappings
	global shift_on

	with open('keycodes.json') as json_file:
		mappings = json.load(json_file)

	with open('shift_on.nfo') as set_file:
		shift_on = set(set_file.read().split(" "))
		shift_on.remove('')

if __name__== "__main__":
	init_maps()
	print(mappings)
	print(shift_on)

	sio.connect('http://softarch.usc.edu:3000/')
	sio.wait()


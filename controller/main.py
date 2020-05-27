import socketio
import logging
import struct
import string
import json

from processing import *

# Set the appropriate log level.
logging.basicConfig(level=logging.DEBUG)

class Event:
    def __init__(self, data):
            self.__dict__ = json.loads(data)

sio = socketio.Client()

@sio.event
def connect():
	global eventProcessor
	logging.info('Connection established!')
	eventProcessor.calibratePointer()
	logging.info('Moving the pointer to the 0, 0!')

@sio.event
def disconnect():
	logging.error('Websocket disconnected.')

# event_console2server
@sio.on('event_server2client')
def event_server2client(data):
	global eventProcessor

	logging.debug(data)
	event = Event(data)

	if event.type != 'mouse':
		logging.error("WRONG CALLBACK! Non mouse_click in event_server2client")
		return
	
	logging.debug("Event.Type: -%s-", event.type)
	if(event.subtype == 'press'):
		click= True;
	else:
		click = False;
	# TODO: Add tracking, not just clicking.
	eventProcessor.executeMouseCommand(event.xPercentage, event.yPercentage, click)

@sio.on('event_server2client_keyboard')
def event_server2client_keyboard(data):
	event = Event(data)

	if event.type == 'mouse':
		logging.error("WRONG CALLBACK! mouse_click in event_server2client_keyboard")
		return

	logging.debug(data)
	logging.debug("Type: -%s-", event.type)
	logging.debug("key: -%s-", event.val)
	eventProcessor.execute_keyboard_command(event.val)

#@sio.on('event_server2client_calibrate')
#def event_server2client_calibrate(data):
#	eventProcessor.calibratePointer();

mappings, shiftOn = loadMappings()
eventProcessor = EventProcessor(mappings, shiftOn, logging)

if __name__== "__main__":

	sio.connect('http://192.168.1.126:3000/')
	sio.wait()

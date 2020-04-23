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

	event = Event(data)

	if event.type != 'mouse_click':
		logging.error("WRONG CALLBACK! Non mouse_click in event_server2client")
		return
	
	logging.debug(data)
	logging.debug("Event.Type: -%s-", event.type)
	
	eventProcessor.executeMouseCommand(event.xPercentage, event.xPercentage, True)

@sio.on('event_server2client_keyboard')
def event_server2client_keyboard(data):
	event = Event(data)

	if event.type == 'mouse_click':
		logging.error("WRONG CALLBACK! mouse_click in event_server2client_keyboard")
		return

	logging.debug(data)
	logging.debug("key: -%s-", event.type)


mappings, shiftOn = loadMappings()
eventProcessor = EventProcessor(mappings, shiftOn, logging)

if __name__== "__main__":

	sio.connect('http://softarch.usc.edu:3000/')
	sio.wait()
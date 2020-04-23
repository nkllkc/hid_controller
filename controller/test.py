import logging
import struct
import string
import json

import fileinput

from processing import *

# Set the appropriate log level.
logging.basicConfig(level=logging.DEBUG)

if __name__== "__main__":
	mappings, shiftOn = loadMappings()
	eventProcessor = EventProcessor(mappings, shiftOn, logging,)

	for line in fileinput.input():
		try:
			args = line.split(' ')
			x = float(args[0])
			y = float(args[1])
			eventProcessor.execute_mouse_command(x, y, args[2][0] == 'y')
		except:
			break

import json
from .configs import *

def loadMappings(mappingFile = 'keycodes.json', shiftOnFile = 'shift_on.nfo'):
    with open(mappingFile) as json_file:
		mappings = json.load(json_file)
        
    with open(shiftOnFile) as set_file:
		shiftOn = set(set_file.read().split(" "))
		shiftOn.remove('')

    return mappings, shiftOn

class EventProcessor:

    def __init__(self, mappings, shiftOn, logging, calibrate = True, hidFile = '/dev/hidg0'):
        self.mappings = mappings
        self.shiftOn = shiftOn
        self.logging = logging
        self.hidFile
        if calibrate:
            self.calibrate_pointer()
        super().__init__()

    def write_report(self, report):
    	with open(self.hidFile, 'rb+') as fd:
    		fd.write(report.encode())	

    # Move the pointer to upper-left corner.
    def calibrate_pointer(self):
    	self.currentX = 0
    	self.currentY = 0

        self.logging.debug("CALIBRATING")

        # TODO: Make this move diagonal.
    	for i in range (0, WIDTH):
    		write_report(LEFT_STEP_REPORT)
    	for i in range (0, HEIGHT):
    		write_report(UP_STEP_REPORT)
    
    def createReportFromKey(self, key):
        if key.islower():
	    	string = NULL_CHAR * 2 + chr(self.mappings[key]) + NULL_CHAR * 5
        elif key.isupper():
	    	string = SHIFT_CHAR + NULL_CHAR + chr(self.mappings[key.lower()]) + NULL_CHAR * 5
        else:
	    	if key not in mappings:
	    		self.logging.debug("Missing key: %s!", key)
	    		return
	    	if key in self.shift_on:
	    		string = chr(32) + NULL_CHAR + chr(self.mappings[key]) + NULL_CHAR * 5
	    	else:
	    		string = NULL_CHAR * 2 + chr(self.mappings[key]) + NULL_CHAR * 5
        return string

    def execute_keyboard_command(self, key):
        self.logging.debug("PRESSED %s", key)
        string = self.createReportFromKey(key)
        self.write_report(string)


    def execute_mouse_command(self, xPercentage, yPercentage, click):	
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
	    	write_report(TOUCH_REPORT)

    
	    self.currentY = newY
	    self.currentX = newX
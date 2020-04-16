import socketio
import logging
import struct
import string
import event_type

# Set the appropriate log level.
logging.basicConfig(level=logging.DEBUG)

def write_report(report):
		with open('/dev/hidg0', 'rb+') as fd:
			fd.write(report.encode())
			null_report = NULL_CHAR * 8
			fd.write(null_report.encode())

def execute_command(key):
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
	write_report(string)



sio = socketio.Client()

@sio.event
def connect():
	logging.info('Connection with GCP is established. Using WebSockets.')

@sio.event
def disconnect():
	logging.error('Disconnected from the GCP GAE.')

@sio.on('event_server2client_keyboard')
def event_server2client_keyboard(data):
	event = event_type.EventType(data)

	logging.debug(data);
	logging.debug("key: -%s-", event.key)
	execute_command(event.key)

shift_on = set()
NULL_CHAR = chr(0)
mappings = {}

if __name__== "__main__":
		
	counter = 4
	for char in string.ascii_lowercase:
		mappings.update({char : counter})
		counter = counter + 1
	backup_counter = counter
	for i in range(1, 10):
		mappings.update({str(i) : counter})
		counter = counter + 1
	mappings.update({"0" : counter})
	mappings.update({")" : counter})
	shift_on.add(")")
	counter = backup_counter
	mappings.update({"!" : counter})
	shift_on.add("!")
	counter = counter + 1
	mappings.update({"@" : counter})
	shift_on.add("@")
	counter = counter + 1
	mappings.update({"#" : counter})
	shift_on.add("#")
	counter = counter + 1
	mappings.update({"$" : counter})
	shift_on.add("$")
	counter = counter + 1
	mappings.update({"%" : counter})
	shift_on.add("%")
	counter = counter + 1
	mappings.update({"^" : counter})
	shift_on.add("^")
	counter = counter + 1
	mappings.update({"&" : counter})
	shift_on.add("&")
	counter = counter + 1
	mappings.update({"*" : counter})
	shift_on.add("*")
	counter = counter + 1
	mappings.update({"(" : counter})
	shift_on.add("(")
	counter = counter + 2
	mappings.update({"Enter" : counter})
	counter = counter + 1
	mappings.update({"Escape" : counter})
	counter = counter + 1
	mappings.update({"Backspace" : counter})
	counter = counter + 1
	mappings.update({"Tab" : counter})
	counter = counter + 1
	mappings.update({" " : counter})
	counter = counter + 1
	mappings.update({"-" : counter})
	mappings.update({"_" : counter})
	shift_on.add("_")
	counter = counter + 1
	mappings.update({"=" : counter})
	mappings.update({"+" : counter})
	shift_on.add("+")
	counter = counter + 1
	mappings.update({"[" : counter})
	mappings.update({"{" : counter})
	shift_on.add("{")
	counter = counter + 1
	mappings.update({"}" : counter})
	shift_on.add("}")
	mappings.update({"]" : counter})
	counter = counter + 1
	mappings.update({"\\" : counter})
	mappings.update({"|" : counter})
	shift_on.add("|")
	counter = counter + 1
	mappings.update({"UNDEF__NON_US_#" : counter})
	mappings.update({"UNDEF__~2" : counter})
	counter = counter + 1
	mappings.update({";" : counter})
	mappings.update({":" : counter})
	shift_on.add(":")
	counter = counter + 1
	mappings.update({'"' : counter})
	mappings.update({"'" : counter})
	shift_on.add("'")
	counter = counter + 1
	mappings.update({"`" : counter})
	mappings.update({"~" : counter})
	shift_on.add("~")
	counter = counter + 1
	mappings.update({"," : counter})
	mappings.update({"<" : counter})
	shift_on.add("<")
	counter = counter + 1
	mappings.update({"." : counter})
	mappings.update({">" : counter})
	shift_on.add(">")
	counter = counter + 1
	mappings.update({"/" : counter})
	mappings.update({"?" : counter})
	shift_on.add("?")
	counter = counter + 1
	mappings.update({"CapsLock" : counter})
	counter = counter + 1
	mappings.update({"F1" : counter})
	counter = counter + 1
	mappings.update({"F2" : counter})
	counter = counter + 1
	mappings.update({"F3" : counter})
	counter = counter + 1
	mappings.update({"F4" : counter})
	counter = counter + 1
	mappings.update({"F5" : counter})
	counter = counter + 1
	mappings.update({"F6" : counter})
	counter = counter + 1
	mappings.update({"F7" : counter})
	counter = counter + 1
	mappings.update({"F8" : counter})
	counter = counter + 1
	mappings.update({"F9" : counter})
	counter = counter + 1
	mappings.update({"F10" : counter})
	counter = counter + 1
	mappings.update({"F11" : counter})
	counter = counter + 1
	mappings.update({"F12" : counter})
	counter = counter + 1
	mappings.update({"PrintScreen" : counter})
	counter = counter + 1
	mappings.update({"ScrollLock" : counter})
	counter = counter + 1
	mappings.update({"Pause" : counter})
	counter = counter + 1
	mappings.update({"Insert" : counter})
	counter = counter + 1
	mappings.update({"Home" : counter})
	counter = counter + 1
	mappings.update({"PageUp" : counter})
	counter = counter + 1
	mappings.update({"DeleteForward" : counter})
	counter = counter + 1
	mappings.update({"End" : counter})
	counter = counter + 1
	mappings.update({"PageDown" : counter})
	counter = counter + 1
	mappings.update({"ArrowRight" : counter})
	counter = counter + 1
	mappings.update({"ArrowLeft" : counter})
	counter = counter + 1
	mappings.update({"ArrowDown" : counter})
	counter = counter + 1
	mappings.update({"ArrowUp" : counter})
	counter = counter + 1

	print(mappings)

	sio.connect('http://softarch.usc.edu:3000/')
	sio.wait()


	print(mappings)

#	for line in fileinput.input():
#		if line.rstrip() == "exit":
#			break
#		for char in line.rstrip():
#			if char.islower():
#				string = NULL_CHAR * 2 + chr(mappings[char]) + NULL_CHAR * 5
#			elif char.isupper():
#				string = chr(32) + NULL_CHAR + chr(mappings[char.lower()]) + NULL_CHAR * 5
#			else:
#				print("ELSE")
#				continue
			#string = string + NULL_CHAR + mappings[char] + NULL_CHAR * 5
#			print("+")
#			write_report(string)
#
			#output_file.write(string.encode())
			#print(char, ord(char))

#	output_file.close()


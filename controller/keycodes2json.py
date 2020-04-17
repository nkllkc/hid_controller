import json
import string


shift_on = set()
NULL_CHAR = chr(0)
mappings = {}

def init_maps(mappings):
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

def getSetString(mySet):
	res = ''
	i = 0
	for x in mySet:
		i += 1
		res += x + " "
	print(i)
	return res

if __name__== "__main__":
	init_maps(mappings)

	r = json.dumps(mappings)
	with open("keycodes.nfo", "w") as fd:
		fd.write(r)

	with open("shift_on.nfo", "w") as fd:
		fd.write(getSetString(shift_on))
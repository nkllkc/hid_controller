# TODO: Make this configurable.
WIDTH = 48
HEIGHT = 86

NULL_CHAR = chr(0)
SHIFT_CHAR = chr(32)

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

NULL_REPORT = NULL_CHAR * 8

# Write a charachter followed by NULL_REPORT.
RIGHT_STEP_REPORT = NULL_CHAR * 2 + chr(RIGHT_ARROW) + NULL_CHAR * 5 + NULL_REPORT
LEFT_STEP_REPORT = NULL_CHAR * 2 + chr(LEFT_ARROW) + NULL_CHAR * 5 + NULL_REPORT
DOWN_STEP_REPORT = NULL_CHAR * 2 + chr(DOWN_ARROW) + NULL_CHAR * 5 + NULL_REPORT
UP_STEP_REPORT = NULL_CHAR * 2 + chr(UP_ARROW) + NULL_CHAR * 5  + NULL_REPORT
TOUCH_REPORT = NULL_CHAR * 2 + chr(TOUCH) + NULL_CHAR * 5  + NULL_REPORT
PRESS_REPORT = NULL_CHAR * 2 + chr(PRESS) + NULL_CHAR * 5  + NULL_REPORT
RELEASE_REPORT = NULL_CHAR * 2 + chr(RELEASE) + NULL_CHAR * 5  + NULL_REPORT


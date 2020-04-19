#!/bin/bash
./cleaner.sh airmochi_emulated_mouse

cd /sys/kernel/config/usb_gadget/
mkdir -p airmochi_emulated_mouse
cd airmochi_emulated_mouse
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Nikola Lukic" > strings/0x409/manufacturer
echo "AirMochi Emulated Mouse" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "conf1" > configs/c.1/strings/0x409/configuration
echo 100 > configs/c.1/MaxPower

# Add functions here
mkdir -p functions/hid.usb1

echo 2 > functions/hid.usb1/protocol
echo 0 > functions/hid.usb1/subclass

# Generic Keyboard.
# echo 8 > functions/hid.usb0/report_length

# Generic Mouse.
# echo 3 > functions/hid.usb0/report_length

# Vertical Mouse.
echo 6 > functions/hid.usb1/report_length

# echo -ne  > functions/hid.usb0/report_desc

# Generic Keyboard.
# echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc

# Generic Mouse.
# echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x02\\x81\\x06\\xc0\\xc0 > functions/hid.usb0/report_desc

# Vertical Mouse.
echo -ne \\x05\\x01\\x09\\x02\\xA1\\x01\\x09\\x01\\xA1\\x00\\x05\\x09\\x19\\x01\\x29\\x06\\x15\\x00\\x25\\x01\\x95\\x06\\x75\\x01\\x81\\x02\\x95\\x02\\x75\\x01\\x81\\x01\\x05\\x01\\x09\\x30\\x09\\x31\\x16\\x01\\x80\\x26\\xFF\\x7F\\x75\\x10\\x95\\x02\\x81\\x06\\xC0\\xA1\\x00\\x95\\x01\\x75\\x08\\x05\\x01\\x09\\x38\\x15\\x81\\x25\\x7F\\x81\\x06\\xC0\\xC0 > functions/hid.usb1/report_desc

# Absolute Mouse.
# echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x35\\x00\\x46\\x9d\\x0b\\x15\\x00\\x26\\x9d\\x0b\\x65\\x11\\x55\\x0e\\x75\\x10\\x95\\x02\\x81\\x02\\xc0\\xc0 > functions/hid.usb0/report_desc


ln -s functions/hid.usb1 configs/c.1/
# End functions

ls /sys/class/udc > UDC
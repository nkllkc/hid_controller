 #!/bin/bash
./cleaner.sh airmochi_emulated_keyboard

cd /sys/kernel/config/usb_gadget/
mkdir -p airmochi_emulated_keyboard
cd airmochi_emulated_keyboard
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Nikola Lukic" > strings/0x409/manufacturer
echo "AirMochi Emulated Keyboard" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "conf1" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

# echo -ne \\x05\\x01\\x09\\x06\\xA1\\x01\\x05\\x07\\x19\\xE0\\x29\\xE7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x01\\x95\\x03\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x03\\x91\\x02\\x95\\x01\\x75\\x05\\x91\\x01\\x95\\x06\\x75\\x08\\x15\\x00\\x26\\xFF\\x00\\x05\\x07\\x19\\x00\\x2A\\xFF\\x00\\x81\\x00\\xC0 > functions/hid.usb0/report_desc
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/
# End functions

ls /sys/class/udc > UDC

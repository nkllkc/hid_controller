#!/bin/bash

if [ $# -eq 1 ]
then
    cd /sys/kernel/config/usb_gadget/$1

    # Disabling the gadget.
    echo "" > UDC

    # Remove functions from configurations.
    rm configs/c.1/hid.usb0

    # Remove strings directories in configurations.
    rmdir configs/c.1/strings/0x409

    # Remove the configurations.
    rmdir configs/c.1

    # Remove functions.
    rmdir functions/hid.usb0

    # Remove strings.
    rmdir strings/0x409

    # Remove the gadget.
    cd ..
    rmdir $1
else
    echo "Argument is missing!"
fi




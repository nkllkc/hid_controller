# rpi_keyboard

This repository contains HID emulator for iOS 13+, based on Raspberry Pi Zero. The reason for using it is that it can act as a USB gadget. This is enables by its support for USB OTG (On-The-Go). It gives the ability to a device to act as either USB host or USB device.

## Setup

### Step 0

Download and install the latest Raspbian Jessie onto a suitably large SD card, and expand the root partition. Make sure you are running kernel 4.4 or later. You can update the kernel by running:
```bash
    sudo BRANCH=next rpi-update
```

### Step 1

#### Device Tree Overlay

Raspberry Pi kernels and firmware use a Device Tree (DT) to describe the hardware present in the Pi. DT overlays allow optional external hardware to be described and configured. 

Overlays are optional elements added to the Device Tree. They enable on the fly functionality, there is no need for re-installing kernel in order for them to take affect. But, you need to reboot your system once you add additional overlay.

https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf - PAGE 56 

In order to run the main program of controller, you need to install python-socketio for Python3:
``
    pip3 install python-socketio
``

Then, you run it with:
``
    python3 main.py
``
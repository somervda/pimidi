#!/usr/bin/python3
# Main pimidi program started by the systemctrl pimidi.service 
# Tasks
# - Show the IP and hostname of the pimidi device (Indicates the device can be used)
# - Start the flask services

import socket
import os

import sys
sys.path.append("/home/pi/pimidi")

gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
ipaddr = s.getsockname()[0]
gateway = gw[2]
host = socket.gethostname()
print ("IP:", ipaddr, " GW:", gateway, " Host:", host)

# Import all board pins.
from board import SCL, SDA
import busio
# Import the SSD1306 module.
import adafruit_ssd1306
# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
display.fill(0)
display.show()
# Note I forced the filename of the font , when run with systemd
# the framebuffer was not finding the font in the default location
display.text(ipaddr, 20, 0, 1,font_name="/home/pi/pimidi/font5x8.bin")
display.show()

#!/usr/bin/python3
# Main pimidi program started by the systemctrl pimidi.service 
# Tasks
# - Show the IP and hostname of the pimidi device (Indicates the device can be used)
# - Start the flask services

import socket
import os
gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
ipaddr = s.getsockname()[0]
gateway = gw[2]
host = socket.gethostname()
print ("IP:", ipaddr, " GW:", gateway, " Host:", host)

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

def do_nothing(obj):
    pass

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial)
device.cleanup = do_nothing
device.show
with canvas(device) as draw:
    draw.text((0, 0), host, fill="white")
    draw.text((0, 15), ipaddr, fill="white")

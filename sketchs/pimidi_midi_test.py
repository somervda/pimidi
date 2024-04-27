#!/usr/bin/python3
import sys
sys.path.append("lib")


# Using https://github.com/edthrn/py-midi as simple midi to serial port interface
# Make sure serial0 is enanbled by using the raspi-config utility and going to
# periferals ->serial (Dont turn on logon shell but do enable serial)
#  On a rpi zero 2w it show up as /dev/serial0
# Set the baud rate by typing  stty -F /dev/serial0 ospeed 31250 (Set to output at midi baud rate)
# echo "Hello" > /dev/serial0

import time

from midi import MidiConnector
from midi import NoteOn
from midi import NoteOff
from midi import Message
for n in range(40,100):
    conn = MidiConnector('/dev/serial0')
    non = NoteOn(n, 127)
    print(n)
    msg = Message(non, channel=1)
    conn.write(msg)
    time.sleep(.1)
    noff = NoteOff(n, 127)
    msg = Message(noff, channel=1)
    conn.write(msg)
    time.sleep(.1)
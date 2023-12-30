#!/usr/bin/python3
# Using https://github.com/edthrn/py-midi as simple midi to serial port interface
# Make sure seria0 is enanbled by using the raspi-config utility and going to
# periferals ->serial (Dont turn on logon shell but do enable serial)
#  On a rpi zero 2w it show up as /dev/serial0
# Set the baud rate by typing  stty -F /dev/serial0 31250 (Set to midi baud rate)

import time

from midi import MidiConnector
from midi import NoteOn
from midi import NoteOff
from midi import Message

conn = MidiConnector('/dev/ttyS1')
non = NoteOn(60, 127)
msg = Message(non, channel=1)
conn.write(msg)
time.sleep(1)
noff = NoteOff(60, 127)
msg = Message(noff, channel=1)
conn.write(msg)
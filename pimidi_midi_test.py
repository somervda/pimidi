#!/usr/bin/python3
# Using https://github.com/edthrn/py-midi as simple midi to serial port interface

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
msg = Message(non, channel=1)
conn.write(msg)
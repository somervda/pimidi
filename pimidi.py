#!/usr/bin/python3

import time
import asyncio
from midiio import MidiIO

o = MidiIO()

o.cv_midi_offset=0
o.noteOn(50)
time.sleep(4)
o.noteOff(50)
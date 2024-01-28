#!/usr/bin/python3

from midiio import MidiIO

o=MidiIO()
print(o.cv_max_volts)
o.cv_max_volts=4.5
print(o.cv_max_volts)
o.settingsSave()
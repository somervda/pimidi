#!/usr/bin/python3
import sys
sys.path.append("lib")
# Set the DAC to the lowest and highest values to measure the highest voltage output
# and measure the frequency produced at the lowest voltage
# Put the calibration results in the settings.json file

import time
import asyncio
from midiio import MidiIO

o = MidiIO()


print("High voltage for 10 seconds, measure CV voltage...")
o.cvSetValue(4095,True)
time.sleep(10)
o.cvSetValue(4095,False)
print("Low voltage for 10 seconds, measure Osc frequency...")
o.cvSetValue(0,True)
time.sleep(10)
o.cvSetValue(0,False)
print("Done!")
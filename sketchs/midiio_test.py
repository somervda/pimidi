#!/usr/bin/python3

import time
import asyncio
from midiio import MidiIO

def play():
    for x in range(48, 90, 4):
        o.noteOn(x)
        time.sleep(3)
        o.noteOff(x)

async def asycPlay():
    print("start noteplay")
    task = asyncio.create_task(o.notePlay(50, 3))
    print("end noteplay - should see this before note finishes playing")
    await task
    print("finish main")

o = MidiIO()

print("* Basic getter, setter tests *")
o.cv_max_volts = o.cv_max_volts
print("cv_max_volts:", o.cv_max_volts)
o.cv_midi_channel = o.cv_midi_channel
print("cv_midi_channel:", o.cv_midi_channel)
o.cv_min_hertz = o.cv_min_hertz
print("cv_min_hertz:", o.cv_min_hertz)
o.midi_display = o.midi_display
print("midi_display:", o.midi_display)
o.midi_default_channel = o.midi_default_channel
print("midi_default_channel:", o.midi_default_channel)
o.cv_midi_offset = o.cv_midi_offset
print("cv_midi_offset:", o.cv_midi_offset)
o.settingsSave()

# *** test midi and cv functions ***
print("* Test  CV tracking functions")
print("CV at unison")
o.cv_midi_offset=0
play()
print("CV at third interval")
o.cv_midi_offset=4
play()
print("Turn off cv tracking")
o.cv_midi_channel=2
o.cv_midi_offset=0
play()

o.cv_midi_channel=1
# *** Test asynchronous note playing ***
print("* Test asyncro function")
asyncio.run(asycPlay())


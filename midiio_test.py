#!/usr/bin/python3

import time
import asyncio

from midiio import MidiIO

o = MidiIO()

def simplePlay():
    for x in range(50, 66, 3):
        o.noteOn(x)
        time.sleep(1)
        o.noteOff(x)

async def main():
    print("start noteplay")
    task = asyncio.create_task(o.notePlay(50, 2))
    print("end noteplay - should see this before note finishes playing")
    await task
    print("finish main")

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

print("* Test  CV tracking functions")
print("CV at unison")
o.cv_midi_offset=0
simplePlay()
print("CV at Major 9th interval")
o.cv_midi_offset=13
simplePlay()
print("CV at Major 7th interval")
o.cv_midi_offset=11
simplePlay()
print("CV at third interval")
o.cv_midi_offset=4
simplePlay()
print("Turn off cv tracking")
o.cv_midi_channel=2
simplePlay()
print("* Test asyncro function")
asyncio.run(main())
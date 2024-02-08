#!/usr/bin/python3

import time
import asyncio

from midiio import MidiIO

o = MidiIO()


async def main():
    print("start noteplay")
    task = asyncio.create_task(o.notePlay(44, 2))
    print("end noteplay")
    await task
    for x in range(40, 72, 1):
        task = asyncio.create_task(o.notePlay(x, 0.1))
        await task
        task = asyncio.create_task(o.notePlay(x , 0.1))
        await task
        await asyncio.sleep(.2)
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

print("* Test asyncronous functions")
asyncio.run(main())

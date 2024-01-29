#!/usr/bin/python3

import time
import asyncio

from midiio import MidiIO

async def main():
    o = MidiIO()

    print("start")
    task = asyncio.create_task(o.notePlay(44,1))
    print("end")
    await task
    print("finish")


asyncio.run(main())

# print(o.cv_max_volts)
# o.cv_max_volts=4.5
# print(o.cv_midi_channel)
# o.cv_midi_channel=2
# print(o.cv_min_hertz)
# o.cv_min_hertz=330
# print(o.midi_display)
# o.midi_display=False
# print(o.midi_default_channel)
# o.midi_default_channel=3
# o.settingsSave()

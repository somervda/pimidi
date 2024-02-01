#!/usr/bin/python3

# The main entrypoint for the pimidi application
# Runs in a fastAPI server to accept web service calls
# Note for testing 

import sys
import time
import asyncio
from midiio import MidiIO

# fastAPI 
from typing import Union,Annotated
from fastapi import FastAPI,Path

# Get IP address
import socket
import os


o = MidiIO()
app = FastAPI()

# Show the IP address
gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
ipaddr = s.getsockname()[0]
o.oledText(20,1,ipaddr,refresh=True)

@app.get("/playNote/{note}/{durationMs}")
async def play_note(note: Annotated[int, Path(title="Midi note value",le=127)],
durationMs:Annotated[int, Path(title="Milliseconds to play the note",ge=50,le=4000)]):
    task = asyncio.create_task(o.notePlay(note,durationMs/1000))
    return{True}

@app.get("/midiNoteOn/{note}")
def midi_note_on(note: Annotated[int, Path(title="Midi note value",le=127)]):
    o.noteOn(note)
    return{True}

@app.get("/midiNoteOnC/{note}/{channel}")
def midi_note_on_C(note: Annotated[int, Path(title="Midi note value",le=127)],
    channel: Annotated[int, Path(title="Midi channel",ge=1,le=16)]):
    o.noteOn(note,channel=channel)
    return{True}

@app.get("/midiNoteOnCV/{note}/{channel}/{velocity}")
def midi_note_on_CV(note: Annotated[int, Path(title="Midi note value",le=127)],
channel: Annotated[int, Path(title="Midi channel",ge=1,le=16)],
    velocity: Annotated[int, Path(title="Note velocity",le=127)]):
    o.noteOn(note,velocity=velocity,channel=channel)
    return{True}


@app.get("/midiNoteOff/{note}")
def midi_note_off(note: Annotated[int, Path(title="Midi note value",le=127)]):
    o.noteOff(note)
    return{True}

@app.get("/midiNoteOffC/{note}/{channel}")
def midi_note_off_C(note: Annotated[int, Path(title="Midi note value",le=127)],
    channel: Annotated[int, Path(title="Midi channel",ge=1,le=16)]):
    o.noteOff(note,channel=channel)
    return{True}

@app.get("/midiNoteOffCV/{note}/{channel}/{velocity}")
def midi_note_off_CV(note: Annotated[int, Path(title="Midi note value",le=127)],
    channel: Annotated[int, Path(title="Midi channel",ge=1,le=16)],
    velocity: Annotated[int, Path(title="Note velocity",le=127)]):
    o.noteOff(note,channel=channel,velocity=velocity)
    return{True}

@app.get("/midiNoteReset")
def midi_note_reset():
    # Reset any active midi notes (incase of a clitch and something got held on)
    for n in range(1,127):
        o.noteOff(n)
    return{True}

# services for getters and setters

@app.get("/CVMaxVolts")
def get_cv_max_volts():
    return(o.cv_max_volts)

@app.get("/CVMaxVolts/{value}")
def set_cv_max_volts(value: Annotated[float, Path(title="CV volts on maximum setting",le=6,gt=0)]):
    o.cv_max_volts=value
    o.settingsSave()
    # Recalc CV tuning and range
    o.cvSettup()
    return True
    
@app.get("/CVMidiChannel")
def get_cv_midi_channel():
    return(o.cv_midi_channel)

@app.get("/CVMidiChannel/{value}")
def set_cv_midi_channel(value: Annotated[int, Path(title="CV midi channel (CV follows this channel)",le=16,gt=0)]):
    o.cv_midi_channel = value
    o.settingsSave()
    return True

@app.get("/CVMinHertz")
def get_cv_min_hertz():
    return(o.cv_min_hertz)

@app.get("/CVMinHertz/{value}")
def set_cv_min_hertz(value: Annotated[float, Path(title="CV minimum hertz (Frequency at zero CV volts)",le=13000,gt=8)]):
    o.cv_min_hertz = value
    o.settingsSave()
    # Recalc CV tuning and range
    o.cvSettup()
    return True

@app.get("/MidiDisplay")
def get_midi_display():
    if o.midi_display:
        return(1)
    else:
        return(0)

@app.get("/MidiDisplay/{value}")
def set_midi_display(value: Annotated[int, Path(title="Show midi output on the display> (1=Yes,0=No)",le=1,ge=0)]):
    if (value==1):
        o.midi_display = True
    else:
        o.midi_display = False
    o.settingsSave()
    return True

@app.get("/MidiDefaultChannel")
def get_midi_default_channel():
    return(o.midi_default_channel)


@app.get("/MidiDefaultChannel/{value}")
def set_midi_default_channel(value: Annotated[int, Path(title="Default Midi channel",le=16,ge=1)]):
    o.mmidi_default_channel = True
    o.settingsSave()
    return True
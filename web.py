#!/usr/bin/python3
# import sys
# sys.path.append("lib")

# The main entrypoint for the pimidi application
# Runs in a fastAPI server to accept web service calls
# Note for testing 
# uvicorn web:app --reload --host pimidi.local

import sys
import time
import json
import asyncio
import os.path
from midiio import MidiIO
import subprocess
from sequence import Sequence

# fastAPI 
from typing import Union,Annotated
from fastapi import FastAPI,Path,Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# Get IP address
import socket
import os


o = MidiIO()
seq = Sequence(quiet=False)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    # Show the IP address
    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[2], 0))
    ipaddr = s.getsockname()[0]
    o.oledText(20,1,ipaddr,refresh=True)
except:
    print("IP address display failed")

# Sequence Services

# @app.get("/sequence/play")
# async def sequencePlay():
#     seq.play()
#     return{True}

@app.get("/sequence/bpm/{bpm}")
async def setBBS(bpm: Annotated[int, Path(title="Beats per second",ge=30,le=800)]):
    seq.bpm = bpm
    return{True}

@app.get("/sequence/ppqn/{ppqn}")
async def setPPQN(ppqn: Annotated[int, Path(title="Pulses per Quarter Note",ge=8,le=128)]):
    seq.ppqn = ppqn
    return{True}

@app.get("/sequence/transpose/{transpose}")
async def setPPQN(transpose: Annotated[int, Path(title="Transpose sequence by n semitones",ge=-12,le=12)]):
    seq.transpose = transpose
    return{True}

@app.get("/sequence/repeat/{repeat}")
async def setRepeat(repeat: Annotated[int, Path(title="Repeat sequence (0=Off,1=On)",ge=0,le=1)]):
    if repeat==0:
        seq.repeat = False
    else:
        seq.repeat = True
    return{True}

@app.get("/sequence/stop")
async def sequenceStop():
    seq.end = True
    return{True}

@app.get("/sequences")
async def sequences():
    return seq.getSequences()

@app.get("/sequence/isPlaying")
async def isPlaying():
    return seq.isPlaying()

@app.get("/sequence/{name}")
async def getSequence(name: Annotated[str, Path(title="Sequence File Name")]):
    # Check if file exists first
    if os.path.isfile("sequences/" + name):
        return seq.getSequence(name)
    else:
        return ""


@app.delete("/sequence/{name}")
async def removeSequence(name: Annotated[str, Path(title="Sequence File Name")]):
    return seq.removeSequence(name)



@app.post("/sequence/play")
async def sequencePlay(request: Request):
    # Use request object to pull the post body that contains the playInfo
    # Save the data to player.json and the default.abc files then start the player
    body = await request.body()
    playInfo = json.loads(body.decode("utf-8"))
    seq.repeat = playInfo.get("repeat", False)
    seq.bpm = playInfo.get("bpm",60)
    seq.transpose = playInfo.get("transpose",0)
    # Save the abc based sequence to default.abc
    seq.abcDefault = playInfo.get("abcDefault","")
    # Start the player
    seq.play()
    return (True)

@app.post("/sequence/save/{name}")
async def saveSequence(name: Annotated[str, Path(title="Sequence File Name")],request:Request):
    # Use request object to pull the post body that contains the abcSequence
    body = await request.body()
    body = json.loads(body.decode("utf-8"))
    print(body)
    return seq.writeSequence(name,body.get("abcSequence",""))

# MIDIIO services

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

@app.get("/cvSetValue/{value}/{on}")
def cv_set_value(value: Annotated[int, Path(title="DAC value",le=4095,ge=0)],
    on: Annotated[int, Path(title="Trigger on or off (0,1)",ge=0,le=1)]):
    # Turn on or off cv based on a DAC VALUE
    if on==1:
        o.cvSetValue(value,True)
    else:
        o.cvSetValue(value,False)
    return{True}

@app.get("/settings")
def get_settings():
    # Special function to get all the settings at once
    return(o.settings)

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

@app.get("/cvMidiOffset")
def get_cv_midi_offset():
    return(o.cv_midi_offset)

@app.get("/cvMidiOffset/{value}")
def set_cv_midi_offset(value: Annotated[int, Path(title="CV Midi offset",le=24,ge=-24)]):
    o.cv_midi_offset=value
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
    o.midi_default_channel = value
    o.settingsSave()
    return True

# Note: Make sure this line is at the end of the file so fastAPI falls through the other
# routes before serving up static files 
app.mount("/", StaticFiles(directory="static", html=True), name="static")
#!/usr/bin/python3

# The main entrypoint for the pimidi application
# Runs in a fastAPI server to accept web service calls

import sys
import time
import asyncio
from midiio import MidiIO

# fastAPI 
from typing import Union,Annotated
from fastapi import FastAPI,Path

o = MidiIO()
app = FastAPI()

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

    



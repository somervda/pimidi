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

@app.get("/midiNoteOff/{note}")
def midi_note_off(note: Annotated[int, Path(title="Midi note value",le=127)]):
    o.noteOff(note)
    return{True}

@app.get("/midiNoteReset")
def midi_note_reset():
    for n in range(1,127):
        o.noteOff(n)
    return{True}

    



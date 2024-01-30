#!/usr/bin/python3

# The main entrypoint for the pimidi application
# Runs a flask server to accept web service calls

import sys
import time
import asyncio
from midiio import MidiIO



from typing import Union

from fastapi import FastAPI

o = MidiIO()
app = FastAPI()

@app.get("/playNote/{note}")
async def play_note(note:int):
    task = asyncio.create_task(o.notePlay(note,1))
    return{1}

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
#!/usr/bin/python3

# Main wrapper for py_midi, ssd1306, mcp4725 and GPIO functionality
import json
import math
import asyncio

# DAC, Midi, OLED and GPIO libraries
import RPi.GPIO as GPIO
import board
import busio

from midi import MidiConnector
from midi import NoteOn
from midi import NoteOff
from midi import Message

import adafruit_mcp4725
import adafruit_ssd1306
import time


class MidiIO:
    MIDINOTE127 = 12543.85
    # Initialize I2C bus.
    i2c = busio.I2C(board.SCL, board.SDA)
    # Initialize MCP4725.
    dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

    def __init__(self):
        # Load pimidi.config (json file)
        try:
            with open('settings.json') as settings_file:
                self.settings = json.load(settings_file)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.strerror, e.filename))
        self.cvSettup()
        self.conn = MidiConnector('/dev/serial0')

    def settingsSave(self):
        with open("settings.json", "w") as settings_file:
            json_settings = json.dumps(self.settings, indent=4)
            settings_file.write(json_settings)

    def noteOn(self,note,channel=None,velocity=127):
        # print("note On",note)
        if channel==None:
            channel=self.midi_default_channel
        noteOn = NoteOn(note, velocity)
        msg = Message(noteOn, channel=channel)
        self.conn.write(msg)

    def noteOff(self,note,channel=None,velocity=127):
        # print("Note off",note)
        if channel==None:
            channel=self.midi_default_channel
        noteOff = NoteOff(note, velocity)
        msg = Message(noteOff, channel=channel)
        self.conn.write(msg)

    async def notePlay(self,note,duration,channel=None,velocity=127):
        self.noteOn(note,channel=channel,velocity=velocity)
        await asyncio.sleep(duration)
        self.noteOff(note,channel=channel,velocity=velocity)


# getters

    @property
    def cv_max_volts(self):
        return self.settings["cv"]["max_volts"]

    @property
    def cv_midi_channel(self):
        return self.settings["cv"]["midi_channel"]

    @property
    def cv_min_hertz(self):
        return self.settings["cv"]["min_hertz"]

    @property
    def midi_display(self):
        return self.settings["midi"]["display"]

    @property
    def midi_default_channel(self):
        return self.settings["midi"]["default_channel"]

# setters
    @cv_max_volts.setter
    def cv_max_volts(self, volts):
        if(volts >= 6):
            raise ValueError("Volts should never be more than 6 volts!")
        self.settings["cv"]["max_volts"] = volts

    @cv_midi_channel.setter
    def cv_midi_channel(self, channel):
        if(channel < 0 or channel > 15):
            raise ValueError("CV can only track midi channels 0 to 15")
        self.settings["cv"]["midi_channel"] = channel

    @cv_min_hertz.setter
    def cv_min_hertz(self, hertz):
        if(hertz < 8.16 or hertz > 13289.75):
            raise ValueError(
                "Midi only supports a frequency range of 8.16 to 13289.75 hertz")
        self.settings["cv"]["min_hertz"] = hertz

    @midi_display.setter
    def midi_display(self, display):
        self.settings["midi"]["display"] = display

    @midi_default_channel.setter
    def midi_default_channel(self, channel):
        if(channel < 0 or channel > 15):
            raise ValueError("Midi only supports channels 0 to 15")
        self.settings["midi"]["default_channel"] = channel


    def cvSettup(self):
        # etFreqStep is the ratio in hertz between 2 adjacent notes in the equal temperament scale (12th root of 2)
        self.etFreqRatio = math.pow(2, 1/12)

        # The ratio in hertz between 2 adjacent dac values going to logarithmic oscillators
        self.cvfreqRatio = math.pow(2, 1/(4095/self.cv_max_volts))
        self.cvMinHertzNoteAndOffset()

    def cvMinHertzNoteAndOffset(self):
        # Find the first midi note above the cv_min_hertz
        for note in range(127, 0, -1):
            noteHertz = self.getMidiNoteHertz(note)
            if (self.cv_min_hertz > noteHertz):
                break
        self.cv_first_midi_note = note + 1
        # Find the DAC value offset to that first note
        for dacOffset in range(0, int((4095/self.cv_max_volts)/12)+1, 1):
            if (self.cv_min_hertz * math.pow(self.cvfreqRatio, dacOffset)) >= self.getMidiNoteHertz(self.cv_first_midi_note):
                self.dacOffset = dacOffset
                break

    def getMidiNoteHertz(self, note):
        return self.MIDINOTE127/(math.pow(self.etFreqRatio, 127-note))

    def settingsPrint(self):
        print(self.settings)

    def oledText(self,x,y,text,refresh=False):
        if refresh:
            self.display.fill(0)
            self.display.show()
        # Note I forced the filename of the font , when run with systemd
        # the framebuffer was not finding the font in the default location
        # See https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/main/adafruit_framebuf.py 
        # fir details of frambuf usage
        self.display.text(text, x, y, 1,font_name="/home/pi/pimidi/font5x8.bin",size=1)
        self.display.show()
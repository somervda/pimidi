#!/usr/bin/python3



# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of setting the DAC value up and down through its entire range
# of values.
import board
import busio

from midi import MidiConnector
from midi import NoteOn
from midi import NoteOff
from midi import Message

import adafruit_mcp4725
import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
# Turn off warnings about gpio possibly being is use.
GPIO.setwarnings(False)
# Using GPIO.BCM mode so channel number is the number after the GPIO desgnation.
GPIO.setmode(GPIO.BCM)
channel=23 
GPIO.setup(channel,GPIO.OUT)


# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725.
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)


dac.raw_value = 4095  # Use the raw_value property to directly read and write
# the 12-bit DAC value.  The range of values is
# 0 (minimum/ground) to 4095 (maximum/Vout).

# Also print send some text to oled to make sure I can do both at once
import adafruit_ssd1306
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

conn = MidiConnector('/dev/serial0')
for x in range(0,769,64):
    # 4095 = 5.38V on my setup
    # 0.0013 volts per step
    # 769 per octave 64 steps per semitone 

    dac.raw_value= x
    GPIO.output(channel,GPIO.HIGH)
    non = NoteOn(42-int((x/64)), 127)
    msg = Message(non, channel=1)
    conn.write(msg)
    print(x, x*0.0013)
    time.sleep(.2)
    GPIO.output(channel,GPIO.LOW)
    noff = NoteOff(42-int((x/64)), 127)
    msg = Message(noff, channel=1)
    conn.write(msg)
    time.sleep(.5)








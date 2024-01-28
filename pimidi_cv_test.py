#!/usr/bin/python3


# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of setting the DAC value up and down through its entire range
# of values.
import board
import busio
import time

import adafruit_mcp4725


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


# Main loop will go up and down through the range of DAC values forever.
while True:
    # Go up the 12-bit raw range.
    print("Going up 0-5V...")
    display.fill(0)
    display.show()
    display.text("Going Up...   ", 0, 10, 1)
    display.show()
    for i in range(4095):
        dac.raw_value = i
    # Go back down the 12-bit raw range.
    print("Going down 5-0V...")
    display.fill(0)
    display.show()
    display.text("Going Down...", 0, 10, 1)
    display.show()
    for i in range(4095, -1, -1):
        dac.raw_value = i

#!/usr/bin/python3


# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
from board import SCL, SDA
import busio

# Import the SSD1306 module.
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
# Clear the display.  Always call show after changing pixels to make the display
# update visible!
display.fill(0)

display.show()
# Note: See framebuf documentation here
# https://docs.circuitpython.org/projects/framebuf/en/latest/ 
display.text("hello world", 0, 0, 1)
display.show()

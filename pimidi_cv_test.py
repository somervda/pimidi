#!/usr/bin/python3



import time

def do_nothing(obj):
    pass

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial)
device.cleanup = do_nothing
device.show
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white",fill="black")
    draw.text((30, 30), "Hello World", fill="white")
time.sleep(3)
device.hide()

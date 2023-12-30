#!/usr/bin/python3

# https://luma-oled.readthedocs.io/en/latest/intro.html 
# Install i2ctools
# sudo apt install -y i2c-tools
# i2cdetect -y 1
# install oled (Luma oled library - quite a few prerequisits)
# sudo apt-get install  python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
# pip3 install --upgrade luma.oled
# sudo usermod -a -G spi,gpio,i2c pi


from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
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

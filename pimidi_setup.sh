#!/usr/bin/env bash

# Before running this file do the following on the raspbery pi
# Add git and your git info
# sudo apt -y install git
# git config --global user.name "pimidi"
# git config --global user.email ""
# git clone https://github.com/somervda/pimidi.git
# This file will now be in the pimidi folder

# It seemd to help to increase the swapfile size of rpi zero device
# I increased it to 140M
# see https://raspberrypi.stackexchange.com/questions/70/how-to-set-up-swap-space
# update /etc/dphys-swapfile  and run  /etc/init.d/dphys-swapfile restart
# Also avoid installing python etc addin when using vscode remote
# The node services dont run well on the memeory space of a RPI zero w 
# https://medium.com/good-robot/use-visual-studio-code-remote-ssh-sftp-without-crashing-your-server-a1dc2ef0936d

# Install prerequisits for PI Midi functionality
# Make sure apt is updated and we have the latest package lists before we start
# Remember to 'chmod u+x pimidi_setup.sh' to be able to run this script 
# then 'bash pimidi_setup.sh'

date
echo 1. Updating and Upgrade apt packages 
sudo apt update -y
sudo apt upgrade -y

echo 2. Installing and rationalizing Python Version Names
sudo apt install -y python-is-python3
sudo apt install -y python3-pip
sudo apt install -y python-dev-is-python3
# Add another path to the python libary folder
# Note: I added an environemnt setting to do the same for 
# the service
echo 'export PYTHONPATH="${PYTHONPATH}:/home/pi/pimidi/lib"' >> ~/.bashrc 


python --version
pip --version

export PATH=$PATH:/home/pi/.local/bin


echo 3. Installing OPi.GPIO 
# Install GPIO support for the orange PI 
# see https://pypi.org/project/RPi.GPIO/ and https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/ 
# Note: Use GPIO.setmode(GPIO.SUNXI) to use "PA01" style channel naming
pip install RPi.GPIO --break-system-packages
# Enable i2c hardware
sudo raspi-config nonint do_i2c 0
# Enable serial hardware but not console thru serial
sudo raspi-config nonint do_serial 2

echo 4. Installing python i2c and oled support
# Adafruit version (Circuit python and python)
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/tree/main 
# Use i2cdetect to make sure you see the i2c device on the I2C 1 bus (Pins 3 and 5)  
# i2cdetect -y 1
echo 4a. Install i2c utilities
#  Can run i2c scans i.e. 'i2cdetect -y 1'
sudo apt-get install -y i2c-tools
# Give pi user access to i2c
sudo usermod -a -G spi,gpio,i2c pi
echo 4b. OLED Installing adafruit i2c and oled support
pip3 install adafruit-circuitpython-ssd1306 --break-system-packages

echo 5. Install adafruit mcp4725 DAC support
# See https://github.com/adafruit/Adafruit_CircuitPython_MCP4725 
pip3 install adafruit-circuitpython-mcp4725  --break-system-packages

pip3 install psutil --break-system-packages

echo 6. Installing midi library for python
# Using https://github.com/edthrn/py-midi 
pip install py-midi  --break-system-packages

echo 7. Install fastapi for web services and a ASGI web server
pip install fastapi  --break-system-packages
pip install "uvicorn[standard]"  --break-system-packages
# Note: I run uvicorn using this command during development
# uvicorn web:app --reload --host pimidi.home


# Add pimidi_uvicorn.service to the /lib/systemd/system/ folder
echo 8. Setup the pimidi_uvicorn.service to run on startup 
sudo cp pimidi_uvicorn.service /lib/systemd/system/pimidi_uvicorn.service
sudo systemctl enable pimidi_uvicorn.service

# Install music21 library to be able to work with ABC music notation
# https://github.com/cuthbertLab/music21
pip install music21  --break-system-packages

# Install mido to support mid file management and playing
# See https://github.com/mido/mido
pip install mido  --break-system-packages

sudo systemctl start pimidi_uvicorn.service 

date

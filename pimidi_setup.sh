#!/usr/bin/env bash

# Before running this file do the following on the raspbery pi
# Add git and your git info
# sudo apt -y install git
# git config --global user.name ""
# git config --global user.email ""
# git clone https://github.com/somervda/pimidi.git
# This file will now be in the pimidi folder

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

python --version
pip --version


echo 3. Installing OPi.GPIO 
# Install GPIO support for the orange PI 
# see https://pypi.org/project/RPi.GPIO/ and https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/ 
# Note: Use GPIO.setmode(GPIO.SUNXI) to use "PA01" style channel naming
pip install RPi.GPIO

echo 4. Installing python oled library
# https://luma-oled.readthedocs.io/en/latest/intro.html 
# Make sure you use raspi-config to set interface options-> I2C to be enabled 
# Use i2cdetect to make sure you see the i2c device on the I2C 1 bus (Pins 3 and 5)  
# i2cdetect -y 1
echo 4b. OLED Installing libjpeg-dev zlib1g-dev
sudo apt install  python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
echo 4c. OLED Installing luma.oled
pip install --upgrade luma.oled
echo 4d. Install i2c utilities
#  Can run i2c scans i.e. 'i2cdetect -y 1'
sudo apt-get install i2c-tools
# Give pi user access to i2c
sudo usermod -a -G spi,gpio,i2c pi

echo 5. Installing midi library for python
# Make sure serial0 is enanbled by using the raspi-config utility and going to
# periferals ->serial (Dont turn on logon shell but do enable serial)
# Using https://github.com/edthrn/py-midi 
pip install py-midi 


# Add pimidi.service to the /lib/systemd/system/ folder
echo 6. Setup the pimidi.service to run on startup
sudo cp pimidi.service /lib/systemd/system/pimidi.service
sudo chmod 644 /lib/systemd/system/pimidi.service
sudo systemctl enable pimidi.service
sudo systemctl daemon-reload

date

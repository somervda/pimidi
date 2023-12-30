#!/usr/bin/env bash
# Install prerequisits for OPI Midi functionality
# Make sure python3 and pip are installed
# Make sure apt is updated and we have the latest package lists before we start
# This whole script takes a while on aOPi zero - maybe 10 minutes
# Remember to 'chmod u+x opimidi_setup.sh' tobe able to run this file 
# then 'bash opimidi_setup.sh'

date
echo 1. Updating and Upgrade apt packages 
sudo apt update -y
sudo apt upgrade -y

echo 2. Install git and set name and email
sudo apt install git
git config --global user.name "somervda"
git config --global user.email "davidsomerville@comcast.net"


echo 3. Rationalizing Python Version Names
sudo apt install -y python-is-python3
sudo apt install -y python-dev-is-python3

python --version
pip --version


echo 4. Installing OPi.GPIO 
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
# Give pi user access to i2c
sudo usermod -a -G spi,gpio,i2c pi

echo 5. Installing midi library for python
# Note: Uses /dev/ttyS2 so make sure UART2 is enables using armbian-config
# Using https://github.com/edthrn/py-midi 
pip install py-midi 
date
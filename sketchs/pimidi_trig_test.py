#!/usr/bin/python3



try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time
# Turn off warnings about gpio possibly being is use.
GPIO.setwarnings(False)
# Using GPIO.BCM mode so channel number is the number after the GPIO desgnation.
GPIO.setmode(GPIO.BCM)

# Test voltage swing and channel usage usage
channel=23 
GPIO.setup(channel,GPIO.OUT)
for x in range(3):
    print("Low")
    GPIO.output(channel,GPIO.LOW)
    time.sleep(.2)
    print("High")
    GPIO.output(channel,GPIO.HIGH)
    time.sleep(.2)
print("Low")
GPIO.output(channel,GPIO.LOW)

channel=24 
GPIO.setup(channel,GPIO.OUT)
for x in range(3):
    print("Low")
    GPIO.output(channel,GPIO.LOW)
    time.sleep(.2)
    print("High")
    GPIO.output(channel,GPIO.HIGH)
    time.sleep(.2)
print("Low")
GPIO.output(channel,GPIO.LOW)



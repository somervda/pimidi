#!/usr/bin/python3
import sys
sys.path.append("lib")


try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
import time
# Turn off warnings about gpio possibly being is use.
GPIO.setwarnings(False)
# Using GPIO.BCM mode so channel number is the number after the GPIO desgnation.
# So GPIO21 is 21 (Which is pin 40 or 40 if ysing GPIO.BOARD mode)
channel=21 
GPIO.setmode(GPIO.BCM)

GPIO.setup(channel,GPIO.OUT)
for x in range(10):
    print("Low")
    GPIO.output(channel,GPIO.LOW)
    time.sleep(.2)
    print("High")
    GPIO.output(channel,GPIO.HIGH)
    time.sleep(.2)
print("Low")
GPIO.output(channel,GPIO.LOW)

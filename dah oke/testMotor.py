#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 17
in2 = 18

# setup
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )

# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.cleanup()

# the meat
try:
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    time.sleep( 2000 )

except KeyboardInterrupt:
    cleanup()
    exit(1)

cleanup()
exit(0)
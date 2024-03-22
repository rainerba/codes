import RPi.GPIO as GPIO
from time import sleep

p = GPIO.PWM(11,50)

def start_servo():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    p.start(7.5)
def CW():
    p.ChangeDutyCycle(5)

def CW_pelan():
    p.ChangeDutyCycle(6.5)

def CCW():
    p.ChangeDutyCycle(10)

def CCW_pelan():
    p.ChangeDutyCycle(8)

def hold():
    p.ChangeDutyCycle(7)
    sleep(5)
    print("Silahkan lanjutkan penalaan . . .")
    return True

def servo_stop():
    p.stop()
    GPIO.cleanup()
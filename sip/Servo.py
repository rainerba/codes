import RPi.GPIO as GPIO
import numpy as np
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12,50)

sleepy=0.4
threshold = 20.

senar = [[6. , 7.9],[6.2 , 7.8],[6.3 , 7.6],[5.7 ,7.9 ],[5.6 , 8.1],[6. , 7.8]]

def start_servo():
    p.start(7)
    
def hold():
    p.ChangeDutyCycle(7)
    sleep(0.1)

def servo_stop():
    p.stop()
    GPIO.cleanup()
    
def map_range(x, in_min, in_max, out_min, out_max):
    if x < -threshold:
        x = -threshold
    elif x > threshold:
        x = threshold
    return (x-in_min)*(out_max-out_min) / (in_max-in_min)+out_min

def main(x, y, pilih):
    if np.abs(x) <= y:
        putar = 7
        return True
    elif x < 0:
        putar = map_range(x, in_min = -threshold, in_max = 0., out_min = 5., out_max = senar[pilih][0])
    elif x > 0:
        putar = map_range(x, in_min = 0., in_max = threshold, out_min = senar[pilih][1], out_max = 10.)
    p.ChangeDutyCycle(putar)
    
if __name__ == '__main__': #gerak di: 7.4, 6.7
    start_servo()
    while True:
        try:
            p.ChangeDutyCycle(float(input("PWM 5-10: ")))
        except KeyboardInterrupt:
            servo_stop()
            break

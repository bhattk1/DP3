from gpiozero import Servo
import gpiozero
import time
import sys
from gpiozero.pins.pigpio import PiGPIOFactory

gpiozero.Device.pin_factory = PiGPIOFactory('127.0.0.1')

servo = Servo(14)

servo.min()
time.sleep(1)
servo.max()

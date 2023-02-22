from gpiozero import Servo
import gpiozero
import time
import sys
from gpiozero.pins.pigpio import PiGPIOFactory

class Actuator:

    def __init__(self,gpioid):
        gpiozero.Device.pin_factory = PiGPIOFactory('127.0.0.1')
        self.id = gpioid
        self.servo = Servo(gpioid)

    def min(self):
        self.servo.min()
        time.sleep(1)

    def max(self):
        self.servo.max()
        time.sleep(1)
from main.sensor_library import *

from gpiozero import Button as gpioButton
import gpiozero
import time
import sys
from gpiozero.pins.pigpio import PiGPIOFactory

class Button:

    def __init__(self,gpioid):
        gpiozero.Device.pin_factory = PiGPIOFactory('127.0.0.1')
        self.id = gpioid
        self.button = gpioButton(gpioid)

    def check_press(self):
        if self.button.is_pressed:
            return True
        else:
            return False
        

def cont_check_button(button_state):
    button = Button(19)
    while True:
        if button.check_press():
            button_state = not button_state
            print("Button Pressed")

cont_check_button(False)

##Note: The code will have to be run on a Command Line or Terminal on a Raspberry Pi, not IDLE since it does not support the multiprocessing functions.

from sensor_library import *

import time,random

from write_temp import Temp_To_Txt as Parser

class ListTemp:
    
    def __init__(self,sensorid) -> None:
        self.templist = []
        self.rollinglist = []
        self.id = sensorid
        if sensorid == 1:
            self.sensor = Temperature_Sensor()

    def getSensorTemp(self) -> float:
        if self.id == 0:
            return float(random.randint(290,300))/10.0
        elif self.id == 1:
            return self.sensor.avg_temp()
        else:
            print("Please input a valid Sensor ID")

    def addTemp(self) -> None:
        self.templist.append(self.getSensorTemp())

    def getRollingTemp(self,rolling_interval,total_time):
        for x in range(0,total_time):
            self.addTemp()
            try:
                if len(self.templist) == rolling_interval:
                    avg = 0
                    for x in range(0,len(self.templist)):
                        avg += self.templist[x]
                    avg = avg/len(self.templist)
                    self.rollinglist.append(avg)
                    self.print_styled(avg)
                    self.templist.pop(0)
            except ZeroDivisionError:
                print("Please input a list of temperatures.")
                return None
            time.sleep(1)

    def print_styled(self,avg):
        str_id = ""
        if self.id == 0:
            str_id = "Standard Temperatures"
        else:
            str_id = "Injured Temperatures "
        print("------",str_id,"-----")
        print("[",end=" ")
        for x in self.templist:
            print(round(x,2),end=" ")
        print("]")
        print("Rolling Avg:",round(avg,2))
        print("----------------------------------")


from gpiozero import Servo
from gpiozero import Button as gpioButton
import gpiozero
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

from multiprocessing import Process as proc
from multiprocessing import Value as val

standardList = ListTemp(0)
injuredList = ListTemp(1)

def standardListInit(rolling,total,rolling_avg):
    standardList.getRollingTemp(rolling,total)

    standard_avg = 0

    for x in standardList.rollinglist:
        standard_avg += x
    
    rolling_avg.value = standard_avg/len(standardList.rollinglist)

def injuredListInit(rolling,total,rolling_avg):
    injuredList.getRollingTemp(rolling,total)
    injured_avg = 0

    for x in injuredList.rollinglist:
        injured_avg += x
    
    rolling_avg.value = injured_avg/len(injuredList.rollinglist)

def cont_check_button(gpioid,button_state):
    button = Button(gpioid)
    while True:
        if button.check_press():
            button_state.value = not button_state.value
            time.sleep(2)
            print("Button pressed")

def cont_check_button_hold(gpioid,time_hold,button_state):
    button = Button(gpioid)
    while True:
        for x in range(0,time_hold+1):
            if button.check_press():
                if x == time_hold:
                    button_state.value = True
                    break
            else:
                break
            time.sleep(1)

def main():
    try:
        servo = Actuator(17)
        button_status = val('b',False)
        button_job = proc(
                    target = cont_check_button,
                args=(19,button_status)
            )
        button_job.start()

        while True:

            while button_status.value:

                svalue = val('d',0.0)
                ivalue = val('d',0.0)

                start = time.perf_counter()

                jobs = []
                
                process1 = proc(
                        target=standardListInit,
                    args=(2,10,svalue)
                )
                jobs.append(process1)

                process2 = proc(
                        target=injuredListInit,
                    args=(2,10,ivalue)
                )
                jobs.append(process2)

                for j in jobs:
                    j.start()

                for j in jobs:
                    j.join()

                for j in jobs:
                    j.terminate()

                stop = time.perf_counter()

                print("Total Time Elapsed: ", stop-start)

                print("Standard Avg Temp:", svalue.value)
                print("Injured Avg Temp:", ivalue.value)

                parser = Parser()

                sval = round(svalue.value,2)
                ival = round(ivalue.value,2)

                parser.write_two_to_file(sval,ival)

                if svalue.value < ivalue.value:
                    print("Servo activated")
                    servo.max()
                    print("sleep")
                    time.sleep(5)
                    print("unsleep")
                else:
                    print("Go next")
                    servo.min()

            while not button_status.value:
                print("Button off")
                time.sleep(3)

    except:
        sys.exit()

if __name__ == "__main__":
    try:
        button_status_hold = val('b',False)
        button_job2 = proc(
                    target = cont_check_button_hold,
                args=(19,3,button_status_hold)
            )
        button_job2.start()

        main_job = proc(
                target = main
        )

        main_job.start()

        while True:
            if button_status_hold.value:
                button_job2.terminate()
                main_job.terminate()
                print("Forced Exit")
                sys.exit()

    except:
        sys.exit()
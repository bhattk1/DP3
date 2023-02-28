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
                    self.templist = []
            except ZeroDivisionError:
                print("Please input a list of temperatures.")
                return None
            time.sleep(1)

from gpiozero import Servo
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

from multiprocessing import Process as proc
from multiprocessing import Value as val

standardList = ListTemp(0)
injuredList = ListTemp(1)

def standardListInit(rolling,total,rolling_avg):
    standardList.getRollingTemp(rolling,total)
    ri = standardList.rollinglist

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

if __name__ == "__main__":

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

    stop = time.perf_counter()

    print("Total Time Elapsed: ", stop-start)

    print("Standard Avg Temp", svalue.value)
    print("Injured Avg Temp", ivalue.value)
    servo = Actuator(14)

    parser = Parser()

    sval = round(svalue.value,2)
    ival = round(ivalue.value,2)

    parser.write_two_to_file(sval,ival)

    if svalue.value < ivalue.value:
        print("Servo activated")
        servo.max()
    else:
        print("Go next")
        servo.min()

import os
import time
import math
import random
from typing import Union

class ListTemp:
    
    def __init__(self,sensorid) -> None:
        self.templist = []
        self.rollinglist = []
        self.id = sensorid
        
    def getList(self) -> list:
        return self.templist

    def getSensorTemp(self) -> float:
        if self.id == 0:
            return float(random.randint(260,300))/10.0
        elif self.id == 1:
            return float(random.randint(260,300))/10.0
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
            str_id = "Injured Temperatures"
        print("------",str_id,"-----")
        print("[ ",end=" ")
        for x in self.templist:
            print(x,end=" ")
        print("]")
        print("Rolling Avg:",round(avg,2))
        print("----------------------------------")
        

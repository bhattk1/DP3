from main.sensor_library import *

from write_temp import Temp_To_Txt as Parser

from average import ListTemp

from actuator import Actuator

import time

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

    print("Standard Avg Temp" + svalue.value)
    print("Injured Avg Temp" + ivalue.value)
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

from sensor_library import *

from average import ListTemp

import time

from multiprocessing import Process as proc

def standardListInit(rolling,total):
    standardList = ListTemp(0)
    standardList.getRollingTemp(rolling,total)
    print(standardList.rollinglist)

def injuredListInit(rolling,total):
    injuredList = ListTemp(1)
    injuredList.getRollingTemp(rolling,total)
    print(injuredList.rollinglist)

if __name__ == "__main__":

    start = time.perf_counter()
    jobs = []
    process1 = proc(
            target=standardListInit,
        args=(2,10)
    )
    jobs.append(process1)
    process2 = proc(
            target=injuredListInit,
        args=(2,10)
    )
    jobs.append(process2)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    for j in jobs:
        j.terminate()

    stop = time.perf_counter()

    print(stop-start)

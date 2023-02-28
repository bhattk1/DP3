##from sensor_library import *
import time as t
from datetime import date,time,datetime
import os

class Temp_To_Txt:
    def __init__(self) -> None:
        pass

    def record_avg_temptotxt(self):
        
        #sensorT = Temperature_Sensor()
        
        while True:
            temps = []
            for i in range(10):
                temps.append(sensorT.avg_temp())
                t.sleep(1)
            avg_temp = sum(temps) / len(temps)
            with open("Temperature Data.txt", "a") as f:
                f.write(str(avg_temp) + "\n")

    def write_to_file(self,item):
        current_date = str(date.today())

        file_name = "Temperature_Data_" + current_date + ".txt"

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        script_dir = os.path.dirname(__file__)
        rel_path = "data\\" + file_name
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, "a") as f:
            f.write(current_time + ":\t" + str(item) + "\n")
            f.close()

    def write_two_to_file(self,item,item2):
        current_date = str(date.today())

        file_name = "Temperature_Data_" + current_date + ".txt"

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        script_dir = os.path.dirname(__file__)
        rel_path = "data\\" + file_name
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, "a") as f:
            f.write(current_time + "\tStandard: " + str(item) + "\tInjured: " + str(item2) + "\n")
            f.close()
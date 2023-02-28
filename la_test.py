from main.sensor_library import *

def main():
    sensor = Temperature_Sensor()
    try:
        while True:
            print(sensor.avg_temp())
    except KeyboardInterrupt:
        print("Forced Exit")

main()
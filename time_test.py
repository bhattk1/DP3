from actuator import Actuator
import time

time.sleep(1)

la = Actuator(17)

for x in range(0,5):
    la.min()
    time.sleep(3)
    la.max()
    time.sleep(3)
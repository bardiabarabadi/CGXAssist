import time
import numpy as np
from CGXAssist.CGX import CGX
from timeit import default_timer as timer

# Create an object from CGX class
device = CGX(timeout=20)
success = device.connect(targetName="NINA-B1-820A11")  # Search for a specific CGX kit device

if not success:
    exit(0)  # Exit if not found

batt = device.getBattery()  # Extract battery info
print("Device battery: " + str(batt))  # Print battery info

device.clearPackets()  # Clear all packets from device memory
time.sleep(5)  # Wait for 5 seconds
device.refresh()
print("Packets in the past 5 seconds:\n" + str(device.packets))

device.decodePackets()

packetRate = np.zeros([200,1])
elapsedTimes = np.zeros([200,1])

for i in range(2):
    start = timer() # Start timer

    device.refresh() # reads a new set of packets from the device
                     # In this function we read all the packets in the buffer of the device and store it
                     # locally (access via device.packets)


    # print("Packets in the past 0.2 seconds:\n" + str(device.packets)) # Uncnomment to print the packets


    packetRate[i] = device.clearPackets() # This is to clear the locally saved packets. Frees up space and improves performance
    end = timer()
    elapsedTimes[i] = end - start # Elsapsed time from start to end
    time.sleep(0.2-elapsedTimes[i][0]) # wait for 0.2 - elapsedTime, i.e. the time spent from "start" to "end"

print ("Mean packet rate: " + str(np.mean(packetRate)))
print ("Mean elapsed time: " + str(np.mean(elapsedTimes)))
device.disconnect()

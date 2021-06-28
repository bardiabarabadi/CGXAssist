import time

from CGXAssist.CGX import CGX

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

device.disconnect()

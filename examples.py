import time

from CGXAssist.CGX import CGX

if __name__ == '__main__':
    deviceName = "NINA-B1-820A11"

    # Create an object from CGX class
    device = CGX(timeout=20)  # This timeout is used for searching and locating a device
    success = device.connect(targetName=deviceName)  # Search for a specific CGX kit device

    if not success:
        exit(0)  # Exit if not found

    batt = device.getBattery()  # Extract battery info
    print("Device battery: " + str(batt))  # Print battery info

    device.clearPackets()  # Clear all packets
    time.sleep(10)  # Wait for 1 second for some packets to arrive
    device.refresh()  # This function transfers the packets from the device buffer to python
    print("RAW packets in the past second:\n" + str(
        device.packets))  # RAW packets are available for debugging purposes in device.packets

    channelContent = device.getChannel(3)

    print(channelContent)

    print("Lost " + str(device.lostPackets) +
    " packets out of " + str(channelContent.shape[0]) + ", i.e " + str(
        100 * (device.lostPackets/(device.lostPackets+channelContent.shape[0]))) + "%")


    device.disconnect()

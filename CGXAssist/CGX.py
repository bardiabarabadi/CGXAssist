from CGXAssist.DeviceFinder import DeviceFinder
import asyncio
import json
from time import time

import bitstring
import numpy as np
from bleak import BleakClient
from bleak.exc import BleakError

from CGXAssist.constants import *

class CGX:

    def __init__(self,
                 loop=None,  # the current eventloop. Only use if using Kivy GUI
                 targetName=None,  # Should be a string containing four digits/letters
                 timeout=30,  # Connection (and search) timeout
                 ):
        self.allDevices = []
        self.targetName = targetName
        self.timeout = timeout

        self.client = None
        self.targetDevice = None
        self.itr = 0
        self.isConnected = False

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.packets=[]
        self.lastPacketCounter = -1
        self.lostPackets = 0

        self.decodedPackets = []


    def disconnect(self):
        self.loop.run_until_complete(self.client.disconnect())
        self.loop.run_until_complete(self.client.disconnect())

    def connect(self, targetName=None):

        if targetName is not None:
            self.targetName = targetName
        elif self.targetName is None:
            print("No target name specified")
            return False

        print ("Searching for BLE device with name=" + str(targetName))
        mf = DeviceFinder()
        self.loop.run_until_complete(mf.search_for_devices(timeout=self.timeout))
        self.allDevices = mf.get_devices()

        if len(self.allDevices) < 1:
            print("Device not found, please try again or increase the timeout")
            return False
        else:
            found = False
            for d in self.allDevices:
                print ("Found BLE device: " + str(d.name))
                if self.targetName.upper() in d.name.upper():
                    print("Target device found. Attempting to connect...")
                    self.targetDevice = d
                    found = True
                    break
            if found is False:
                print("Couldn't find target, + " + str(self.targetName) + ". Try again or increase the timeout.")
                return False

        # Connecting
        self.client = BleakClient(self.targetDevice.address, loop=self.loop)
        try:
            for retry in range(int(self.timeout / 4) + 1):
                try:
                    self.loop.run_until_complete(self.client.connect(timeout=self.timeout))
                    success = True
                except BleakError:
                    success = False
                if success:
                    break
            if not success:
                return False
        except asyncio.exceptions.TimeoutError:
            print("Time out reached, cannot connect to the device! Ty again...")
            return False
        print("connection was successful")

        self.loop.run_until_complete(self.client.start_notify(CGX_STREAM_ATTR, self._streamCallback))
        self.refresh()
        self.isConnected = True
        return True

    def listDevices(self, partialName=None):
        mf = DeviceFinder(partialName=partialName)
        self.loop.run_until_complete(mf.search_for_devices(timeout=self.timeout))
        self.allDevices = mf.get_devices()
        return self.allDevices

    def refresh(self):
        self.loop.run_until_complete(self.client.read_gatt_char('2456E1B9-26E2-8F83-E744-F34F01E9D703'))

    def clearPackets(self):
        self.decodedPackets = []
        numPackets = len(self.packets)
        self.packets=[]
        self.itr=0
        return numPackets

    def decodePackets(self):

        for i, p in enumerate(self.packets):
            decodedPacket = np.zeros([CGX_CHANNEL_COUNT,1])
            counter = int(self.packets[i][0:2*CGX_HEADER_LENGTH_BYTES], 16)

            if self.lastPacketCounter == -1:
                pass
            else:
                if (counter-self.lastPacketCounter) == 1 or (counter-self.lastPacketCounter) == -127:
                    pass
                else:
                    if counter > self.lastPacketCounter:
                        self.lostPackets = self.lostPackets + (counter-self.lastPacketCounter-1)
                    else:
                        self.lostPackets = self.lostPackets + (127 + counter - self.lastPacketCounter - 1)

            self.lastPacketCounter = counter

            for channel in range(CGX_CHANNEL_COUNT):
                hexPayload = self.packets[i][2*(CGX_HEADER_LENGTH_BYTES+1+3*channel):
                                             2*(CGX_HEADER_LENGTH_BYTES+1+3*(channel+1))]
                msb  = int(hexPayload[0:2],16)
                lsb1 = int(hexPayload[2:4],16)
                lsb2 = int(hexPayload[4:6],16)

                decodedPacket[channel]= 2**8 * (msb    * 2**18
                                                + lsb1 * 2**11
                                                + lsb2 * 2**4
                                                )
            self.decodedPackets.append(decodedPacket)
        return self.decodedPackets





    def getBattery(self):
        if len(self.packets) == 0:
            self.refresh()
        hexBattery=self.packets[-1][2*(CGX_OFFSET_TAIL_BYTES+1):2*(CGX_OFFSET_TAIL_BYTES+2)]
        return (int(hexBattery,16)/255)*100

    def _streamCallback(self, sender, packet):
        self.itr=self.itr+1

        bit_decoder = bitstring.Bits(bytes=packet)
        packet_hex = bit_decoder.hex
        receviedPackets = packet_hex.split('ff')
        if len(receviedPackets) <= 1:
            return
        if len(receviedPackets[0]) != (CGX_PACKET_LENGTH_BYTES * 2):
            receviedPackets.pop(0)
        if len(receviedPackets[-1]) != (CGX_PACKET_LENGTH_BYTES * 2):
            receviedPackets.pop(-1)
        self.packets.extend(receviedPackets)


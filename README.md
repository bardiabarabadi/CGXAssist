# CGXAssist

> **Status: unmaintained.** This is an early alpha (0.0.0.dev0) that is no longer developed. It was written against the 2021 `bleak` API and does not work with current `bleak` releases without changes.

A python library to assist developers with CGX EEG dev-kit. It connects to the dev-kit's Bluetooth LE module and decodes the received packets; a MATLAB wrapper is in `MATLAB/`.

## Installation
    pip install CGXAssist
    
## Usage
See [examples.py](https://github.com/bardiabarabadi/CGXAssist/blob/master/examples.py)

## Updates

- Added decodePackets() method which extracts the channel values from all of the recieved packets. Note that the user 
needs to set the correct CGX_CHANNEL_COUNT in constants.py (according the device) to make it work properly. This option 
will be moved to the class __init__ method before Beta release. 
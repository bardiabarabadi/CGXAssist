# CGXAssist

A python library to assist developers with CGX EEG dev-kit.

## Installation
    pip install CGXAssist
    
## Usage
See [examples.py](https://github.com/bardiabarabadi/CGXAssist/blob/master/examples.py)

## Updates

- Added decodePackets() method which extracts the channel values from all of the recieved packets. Note that the user 
needs to set the correct CGX_CHANNEL_COUNT in constants.py (according the device) to make it work properly. This option 
will be moved to the class __init__ method before Beta release. 
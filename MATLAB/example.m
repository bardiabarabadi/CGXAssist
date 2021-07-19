
clear

cgx = CGXAssist("EFB8D9CA-6D9E-4C6F-BFF0-C7EF3A5DCDDC");
cgx = cgx.findAndConnect();

% Start reading from the device
cgx.startStream()
pause(1)
% Stop reading from the device after one second
cgx.stopStream()

% Refresh function translates the RAW values into usable arrays (not
% completed yet)
cgx=cgx.refresh();

% This clears the recieved packets to free up memory. Average memory usage:
% 40kB/sec (TBD)
cgx = cgx.clearPackets();

% This returns the battery in percent
batt = cgx.getBattery();

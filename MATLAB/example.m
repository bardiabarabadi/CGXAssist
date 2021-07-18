
clear

cgx = CGXAssist("EFB8D9CA-6D9E-4C6F-BFF0-C7EF3A5DCDDC");
cgx = cgx.findAndConnect();

cgx.startStream()
pause(10)
cgx.stopStream()
cgx=cgx.refresh()



#!/bin/sh
# Rickie Kerndt <rkerndt@cs.uoregon.edu>
# script to turn off devices for power conservation

# turn off HDMI output
/usr/bin/tvservice -o

# turn off LAN9514 (usb and ethernet) by default, but must have at
# least one interface going so give option to turn off wifi instead
if [ $# -eq 1 -a $1 = "nowifi" ]; then
    # turn off wifi
    /sbin/ifdown wlan0
else
    # disable lan9514
    /usr/local/bin/lan9514 disable
fi
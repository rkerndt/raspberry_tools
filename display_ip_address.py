#!/usr/bin/python
"""
Rickie Kerndt <rkerndt@cs.uoregon.edu>
"""

from __future__ import print_function

print('entering display_ip_address')
UO_GREEN = (0,79,39)
UO_YELLOW = (255,204,0)

MODULE_PATH = '/home/pi/GrovePi/Software/Python/grove_rgb_lcd/grove_rgb_lcd.py'
MODULE_NAME = 'grove_rgb_lcd'
ADDR_STR = 'new_ip_address'

#check to see if new address exists before doing anything else
from os import environ
if (ADDR_STR not in environ) or (len(environ[ADDR_STR]) == 0):
    exit(1)

from sys import stderr
import imp

try:
    grove_rgb_lcd = imp.load_source(MODULE_NAME, MODULE_PATH)
except ImportError:
    msg = 'display_ip_address: failed to find %s module' % MODULE_NAME
    print(msg, file=stderr)
    exit(1)
print('setting lcd to display ip address %s' % environ[ADDR_STR])
grove_rgb_lcd.setRGB(*UO_GREEN)
grove_rgb_lcd.setText(environ[ADDR_STR])
exit(1)

#!/usr/bin/python
"""
Rickie Kerndt <rkerndt@cs.uoregon.edu>
"""

from __future__ import print_function
from os import environ
from sys import stderr
import imp

UO_GREEN = (0,79,39)
UO_YELLOW = (255,204,0)

MODULE_PATH = '/home/pi/GrovePi/Software/Python/grove_rgb_lcd/grove_rgb_lcd.py'
MODULE_NAME = 'grove_rgb_lcd'
ADDR_STR = 'new_ip_address'

print('entering display_ip_address.py')

try:
    grove_rgb_lcd = imp.load_source(MODULE_NAME, MODULE_PATH)
except ImportError:
    msg = 'display_ip_address: failed to find %s module' % MODULE_NAME
    print(msg, file=stderr)
    exit(1)

if (ADDR_STR not in environ) or (len(environ[ADDR_STR]) == 0):
    grove_rgb_lcd.setRGB(*UO_YELLOW)
    grove_rgb_lcd.setText('missing ip addr')
else:
    grove_rgb_lcd.setRGB(*UO_GREEN)
    grove_rgb_lcd.setText(environ[ADDR_STR])

exit(1)

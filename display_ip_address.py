#!/usr/bin/python
"""
Rickie Kerndt <rkerndt@cs.uoregon.edu>
"""

from __future__ import print_function

SEARCH_PATH = '/home/pi/GrovePi/Software/Python'
MODULE_NAME = 'grove_rgb_lcd'
ADDR_STR = 'new_ip_address'

#check to see if new address exists before doing anything else
from os import environ
if (ADDR_STR not in environ) or (len(environ[ADDR_STR]) == 0):
    exit(1)

from sys import stderr
import imp

try:
    filename, pathname, description = imp.find_module(MODULE_NAME,SEARCH_PATH)
except ImportError:
    msg = 'display_ip_address: failed to find %s module' % MODULE_NAME
    print(msg, file=stderr)
    exit(1)

grove_lcd = imp.load_module(filename, pathname, description)

grove_lcd.setText(environ[ADDR_STR])
exit(1)

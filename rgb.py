#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from threading import Thread



class RGB_led:
    """
    Provides methods for manipulating leds on the RGB LED module.
    This will set GPIO mode to BCM if not already set. If you wish to
    use BOARD numbering then be sure to set BOARD mode prior to
    instantiating the RBG_led class.
    """

    BLINK_ON  = 0.1
    BLINK_OFF = 0.9
    RED   = (1,0,0)
    GREEN = (0,1,0)
    BLUE  = (0,0,1)
    OFF   = (0,0,0)
    COLORS = (RED, GREEN, BLUE, OFF)

    def __init__(self, red_pin, green_pin, blue_pin):
        # LED CONFIG - Set GPIO Ports
        self._red_pin = red_pin  # B21
        self._green_pin = green_pin  # B20
        self._blue_pin = blue_pin  # B16
        self._rgb = (self._red_pin, self._green_pin, self._blue_pin)
        self._cycle_thread = None
        self._cycling = False
        self._init_gpio()
        self.clear()


    def close(self):
        """
        Turns off leds and calls cleanup on pins.
        """
        self.clear()
        GPIO.cleanup(self._rgb)

    def clear(self):
        """
        Terminates any cycling thread and turns off all led colors
        """
        if self._cycling:
            self._cycle_stop()

        self._set(*RGB_led.OFF)

    def red(self, blink=False):
        """
        set led to red
        :param blink: True/False
        """
        self._color(RGB_led.RED, blink)

    def green(self, blink=False):
        """
        set led to green with optional blink
        :param blink: True/False
        """
        self._color(RGB_led.GREEN, blink)

    def blue(self, blink=False):
        """
        set led to blue
        :param blink: True/False
        """
        self._color(RGB_led.BLUE, blink)

    def _color(self, color, blink=False):
        """
        Sets led to color and blinks if blink = True
        :param color: one of RED, GREEN, BLUE
        :param blink: True, FALSE
        """
        if color in RGB_led.COLORS:
            if self._cycling:
                self._cycle_stop()
            if blink:
                self._cycle_start( color, RGB_led.OFF, RGB_led.BLINK_ON, RGB_led.BLINK_OFF)
            else:
                self._set(*color)

    def _set(self, red, green, blue):
        """
        Sets LEDs on or off
        :param red: 0 (off) | 1 (on)
        :param blue:  0 (off) | 1 (on)
        :param green:  0 (off) | 1 (on)
        """
        for color in [red, green, blue]:
            if color not in [0,1]:
                raise ValueError

        GPIO.output(self._red_pin, red)
        GPIO.output(self._blue_pin, blue)
        GPIO.output(self._green_pin, green)


    def _cycle_start(self, rgb_a, rgb_b, interval1, interval2):
        """
        Cycles state of led colors rgb_a and rgb_b for interval seconds
        :param rgb_a: tuple (r,g,b)
        :param rgb_b: tuple (r,g,b)
        :param interval1: float seconds with rgb_a set
        :param interval2: float seconds with rgb_b set
        """
        self._cycling = True
        self._cycle_thread = Thread(target=self._cycle, args=(rgb_a, rgb_b, interval1, interval2))
        self._cycle_thread.start()

    def _cycle_stop(self):
        """
        Terminates thread cycling led color
        """
        self._cycling = False
        self._cycle_thread.join()
        self._cycle_thread = None

    def _cycle(self, rgb_a, rgb_b, interval1, interval2):
        """
        Private method launched as thread to cycle led colors
        :param rgb_a:
        :param rgb_b:
        :param interval1:
        :param interval2:
        """

        while self._cycling:
            self._set(*rgb_a)
            time.sleep(interval1)
            self._set(*rgb_b)
            time.sleep(interval2)

    def _init_gpio(self):
        """
        Sets gpio for controlling pins connected to an RGB led. No assumptions are
        made about the pin numbering mode. The mode is first checked and set to BCM
        if found undefined. So, if you wish to use BOARD numbering mode, then set
        this mode prior to instantiating a RGB_led class.
        """
        GPIO.setwarnings(False)
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)

        GPIO.setup(self._rgb, GPIO.OUT)

    def __repr__(self):
        """
        String representation of led configuration
        """
        return('RGB_led(%d,%d,%d)' % (self._red_pin, self._green_pin, self._blue_pin))
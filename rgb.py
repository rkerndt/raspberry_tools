#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from threading import Thread



class RGB_led:
    """
    Provides methods for manipulating leds on the Keyes RGB LED module.
    This will set GPIO mode to BCM if not already set. If you wish to
    use BOARD numbering then be sure to set BOARD mode prior to
    instantiating the RBG_led class.
    """

    def __init__(self, red_pin, green_pin, blue_pin):
        # LED CONFIG - Set GPIO Ports
        self.red_pin = red_pin  # B22
        self.blue_pin = blue_pin  # B21 Rev1  B27 Rev2
        self.green_pin = green_pin  # B17
        self.rgb = (self.red_pin, self.green_pin, self.blue_pin)
        self.cycle_thread = None
        self.cycling = False

        self.__init_gpio()
        self.clear()


    def close(self):
        """
        Turns off leds and calls cleanup on pins.
        """
        self.clear()
        GPIO.cleanup(self.rgb)

    def clear(self):
        """
        Terminates any cycling thread and turns off all led colors
        """
        if self.cycle_thread:
            self.cycle_stop()

        GPIO.output(self.red_pin, 0)
        GPIO.output(self.blue_pin, 0)
        GPIO.output(self.green_pin, 0)

    def set(self, red, blue, green):
        """
        Sets LED on or off
        :param red: 0 (off) | 1 (on)
        :param blue:  0 (off) | 1 (on)
        :param green:  0 (off) | 1 (on)
        """
        for color in [red, blue, green]:
            if color not in [0,1]:
                raise ValueError

        GPIO.output(self.red_pin, red)
        GPIO.output(self.blue_pin, blue)
        GPIO.output(self.green_pin, green)


    def cycle_start(self, rgb_a, rgb_b, interval):
        """
        Cycles state of led colors rgb_a and rgb_b for interval seconds
        :param rgb_a: tuple (r,g,b)
        :param rgb_b: tuple (r,g,b)
        :param interval: float seconds
        """
        self.cycling = True
        self.cycle_thread = Thread(target=self.__cycle, args=(rgb_a, rgb_b, interval))
        self.cycle_thread.start()

    def cycle_stop(self):
        """
        Terminates thread cycling led color
        """
        if self.cycle_thread:
            self.cycling = False
            self.cycle_thread.join()

    def __cycle(self, rgb_a, rgb_b, interval):
        """
        Private method launched as thread to cycle led colors
        :param rgb_a:
        :param rgb_b:
        :param interval:
        """

        while self.cycling:
            self.set(*rgb_a)
            time.sleep(interval)
            self.set(*rgb_b)
            time.sleep(interval)

    def __init_gpio(self):
        """
        Sets gpio for controlling pins connected to an RGB led. No assumptions are
        made about the pin numbering mode. The mode is first checked and set to BCM
        if found undefined. So, if you wish to use BOARD numbering mode, then set
        this mode prior to instantiating a RGB_led class.
        """
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)

        GPIO.cleanup(self.rgb)
        GPIO.setup(self.rgb, GPIO.OUT)


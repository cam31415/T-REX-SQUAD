#!/usr/bin/env pybricks-micropython
'''Hello to the world from ev3dev.org'''

import os
import sys
import time

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
# state constants
ON = True
OFF = False


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


def main():
    '''The main function of our program'''

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')


    ev3 = EV3Brick()
    # moteur
    test_motor = Motor(Port.D)
    test_motor.run_target(1000, 90)

    # son
    ev3.speaker.beep(frequency=1000, duration=500)
    #ev3.speaker.beep(frequency=800, duration=200)
    #ev3.speaker.beep(frequency=1000, duration=500)
    #ev3.speaker.beep(frequency=800, duration=200)


    #ev3.speaker.beep()

#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_B
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.led import Leds
from time import sleep

# Connect infrared and touch sensors to any sensor ports
ir = InfraredSensor() 
leds = Leds()
large_motor = LargeMotor(OUTPUT_B)

leds.all_off() # stop the LEDs flashing (as well as turn them off)
large_motor.on(speed=20)

# is_pressed and proximity are not functions and do not need parentheses
while not large_motor.wait_until_not_moving():  # Stop program by stop motor's moving
    if ir.proximity < 40*1.4: # to detect objects closer than about 40cm
        print(ir.proximity)
        leds.set_color('LEFT',  'RED')
        leds.set_color('RIGHT', 'RED')
    else:
        print(ir.proximity)
        leds.set_color('LEFT',  'GREEN')
        leds.set_color('RIGHT', 'GREEN')

    sleep (0.01) # Give the CPU a rest
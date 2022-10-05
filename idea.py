#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_B
from ev3dev2.sensor.lego import InfraredSensor
from ev3dev2.sound import Sound

sound = Sound()
ir = InfraredSensor() 
large_motor = LargeMotor(OUTPUT_B)

large_motor.on(speed=50)

large_motor.wait_until_not_moving()
sound.speak('I have the high ground !')
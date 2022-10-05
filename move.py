#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_B

large_motor = LargeMotor(OUTPUT_B)

large_motor.on(speed=100)
large_motor.wait_until_not_moving()
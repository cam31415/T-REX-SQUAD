#!/usr/bin/env python3

from time import sleep
from smbus import SMBus

import os
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B,SpeedRPM
from ev3dev2.port import LegoPort
from ev3dev2.sound import Sound

import threading


def limit_speed(speed):
    """ Limit speed in range [-1000,1000] """
    if speed > 100:
        speed = 100
    elif speed < -100:
        speed = -100
    return speed

os.system('setfont Lat15-Terminus24x12 ')

# Set LEGO port for Pixy2 on input port 1
in1 = LegoPort(INPUT_1)
in1.mode = 'other-i2c'
# Short wait for port to get ready
sleep(0.5)

# Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)
# Make sure the same address is set in Pixy2
address = 0x54

# Signatures we're interested in (SIG1)
sigs = 3

# Connect TouchSensor (to stop script)
#ts = TouchSensor(INPUT_2)

# Connect LargeMotors
motor = Motor(OUTPUT_A)
shoot = Motor(OUTPUT_B)

# Defining constants
X_REF = 158  # X-coordinate of referencepoint
Y_REF = 150  # Y-coordinate of referencepoint
KP = 0.4     # Proportional constant PID-controller
KI = 0.01    # Integral constant PID-controller
KD = 0.05    # Derivative constant PID-controller
GAIN = 10    # Gain for motorspeed

# Initializing PID variables
integral_x = 0
derivative_x = 0
last_dx = 0
integral_y = 0
derivative_y = 0
last_dy = 0

# Data for requesting block
data = [174, 193, 32, 2, sigs, 1]



def plachta():
    # Request block
    bus.write_i2c_block_data(address, 0, data)
    # Read block
    block = bus.read_i2c_block_data(address, 0, 20)

    sig = 1
    sig2 = 2
    
    print("sig value is: ", block[6])
    if sig == block[7]*256 + block[6] or sig2 == block[7]*256 + block[6]:
        # SIG1 detected, control motors
        x = block[9]*256 + block[8]   # X-centroid of largest SIG1-object
        w = block[13]*256 + block[12]
        
        
        if x > 316:
            x = 0
        else:
            x = x
        
        if w > 316:
            w = 0
        else:
            w = w
        
        distance = 1316/w
        
    
        # Use GAIN otherwise speed will be to slow,
        # but limit in range [-1000,1000]
        rspeed = limit_speed(GAIN*(-8))
        lspeed = limit_speed(GAIN*(8))
        

        print('%.2f' % x)
        
        if x >= 168 or x <= 148:
            if x >= 168:
                motor.run_forever(speed_sp = round(rspeed))
            else:
                motor.run_forever(speed_sp = round(lspeed))
        else:
            motor.stop()
            shoot.on_for_seconds(speed=SpeedRPM(100), seconds=2)
            print('%.2f' % distance)
        
        return True

    return False
            




if __name__ == "__main__":

    istrack = False
    n = 5
    i = 1
    spkr = Sound()



    while True:
        
        if not istrack:
            motor.on_for_seconds(speed=-n, seconds=1)
            if motor.is_stalled :
                n = -n
                #spkr.speak("Stalled change of direction operate")
                sleep(0.5)
        

        istrack = plachta()
        

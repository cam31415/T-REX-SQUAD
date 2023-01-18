#!/usr/bin/env python3

from time import sleep
from smbus import SMBus

import os
from pixycamev3.pixy2 import Pixy2
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_4,INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B,SpeedRPM, OUTPUT_D,OUTPUT_C
from ev3dev2.port import LegoPort
from ev3dev2.sound import Sound
from time import sleep

import threading

def limit_speed(speed):

    """ Limit speed in range [-1000,1000] """

    if speed > 100:
        speed = 100
    elif speed < -100:
        speed = -100
    return speed


os.system('setfont Lat15-Terminus24x12 ')


# Pixy2 connected to port 1, i2c address set to 0x54
pixy2 = Pixy2(port=1, i2c_address=0x54)


#Connect LargeMotors
motor = Motor(OUTPUT_A)
shoot = Motor(OUTPUT_B)
vertical_motor_1 = Motor(OUTPUT_D)
vertical_motor_2 = Motor(OUTPUT_C)
tsl = TouchSensor(INPUT_2)
tsr = TouchSensor(INPUT_4)

# #Defining constants

GAIN = 10    # Gain for motorspeed

global Flag_Shoot
global Flag_Scanning

Flag_Scanning = True
Flag_Shoot = False

spkr = Sound()



def tracking():
    global Flag_Shoot
    global Flag_Scanning

    while(True):
        # Request blockdata for sig=1, max 1 block
        nr_blocks, block = pixy2.get_blocks(3, 255)

        x = 0
        y = 0

        list_distance = []

        if nr_blocks > 0:
            #sig = block[0].sig
            x = block[0].x_center
            y = block[0].y_center
            w = block[0].width
            h = block[0].height
            Flag_Scanning = False

            distance1 = 1316/w
            list_distance.append(distance1)

            if nr_blocks > 1:

                #spkr.speak("two goals")
                print("there are 2 targets")
                x0 = block[1].x_center
                y0 = block[1].y_center
                w0 = block[1].width
                h0 = block[1].height

                if w > w0:
                    x = x
                    y = y
                else:
                    x = x0
                    y = y0

                distance2 = 1316/w
                list_distance.append(distance2)




            rspeed = limit_speed(GAIN*(-7))
            lspeed = limit_speed(GAIN*(7))

            rspeed0 = limit_speed(GAIN*(-4))
            lspeed0 = limit_speed(GAIN*(4))

            if(nr_blocks > 1):
                print("value of  first:", list_distance[0])
                print("value of  second:", list_distance[1])
            else:
                print("value of  first:", list_distance[0])

            # x-axe calibration
            if x >= 168 or x <= 148:#Make sure the value of x is always around 158
                if x == 0:
                    motor.stop()

                if x >= 168:

                    motor.run_forever(speed_sp = round(rspeed))
                else :
                    motor.run_forever(speed_sp = round(lspeed))


                #print('%.2f' % distance)

            # y-axe calibration
            if y >= 112 or y <= 96:
                if y == 0:
                    vertical_motor_1.stop()
                    vertical_motor_2.stop()
                if y >= 112:
                    vertical_motor_1.run_forever(speed_sp = round(rspeed0))
                    vertical_motor_2.run_forever(speed_sp = round(rspeed0))
                else:
                    vertical_motor_1.run_forever(speed_sp = round(lspeed0))
                    vertical_motor_2.run_forever(speed_sp = round(lspeed0))
            else:

                Flag_Shoot = True
        else:
            if(not Flag_Scanning):
                motor.stop()
            Flag_Scanning = True
            vertical_motor_1.stop()
            vertical_motor_2.stop()
            continue




def shooting():

    global Flag_Shoot

    while(True):

        if(Flag_Shoot):

            shoot.on_for_seconds(speed=SpeedRPM(100), seconds=2)

            Flag_Shoot = False



def scanning():

    n = 50
    global Flag_Scanning
    Flag_Scanning = True
    while True:

        if(Flag_Scanning):
            motor.on_for_seconds(speed=-n, seconds=1)


            #The shooting part turns left and right, and the direction changes when it touches the contact sensor
            if(tsl.is_pressed):

                n = -9

            if(tsr.is_pressed):

                n = 9








if __name__ == "__main__":



    #Run programs in multiple threads
    t1 = threading.Thread(target=tracking)

    t2 = threading.Thread(target=shooting)

    t3 = threading.Thread(target=scanning)



    t1.start()

    t2.start()

    t3.start()








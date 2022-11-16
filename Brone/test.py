#!/usr/bin/env python3
from ast import Break
from time import sleep
from smbus import SMBus
import os
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.port import LegoPort
from ev3dev2.motor import OUTPUT_C,Motor, SpeedRPM, OUTPUT_D, OUTPUT_A, OUTPUT_B
from ev3dev2.sound import Sound
import threading

size_px_init = 60
distance_init = 20
FLAG_END = False

def get_distance_target(n):
    return (size_px_init*distance_init)/n

def pixycam():

    global FLAG_END
    spkr = Sound()
    # Set LEGO port for Pixy2 on input port 1
    in1 = LegoPort(INPUT_1)
    in1.mode = 'other-i2c'
    # Short wait for the port to get ready
    sleep(0.5)

    # Settings for I2C (SMBus(3) for INPUT_1)
    bus = SMBus(3)
    # Make sure the same address is set in Pixy2
    address = 0x54

    # Signatures we're interested in (SIG1)
    sigs = 6

    # Data for requesting block
    data = [174, 193, 32, 2, sigs, 1]

    spkr.speak("Pixy Camera is initiate")
    while 1:
        # Request block
        bus.write_i2c_block_data(address, 0, data)
        # Read block
        block = bus.read_i2c_block_data(address, 0, 20)
        # Extract data
        sig2 = block[6]

        # check red object and calculate distance
        if(sig2 == 2):
            spkr.speak('red color detect')
            w = block[13]*256 + block[12]
            print(get_distance_target(w))
            FLAG_END = True

        if(FLAG_END):
            #spkr.speak('The program it\'s finish ')
            print('Program finish')
            sleep(60)
            break
            #sleep(60)
            #FLAG_END = False



# move right wheel
def rd():
    m_rotation_rd = Motor(OUTPUT_A)
    while True:
        m_rotation_rd.on_for_seconds(SpeedRPM(20), 1)
        sleep(1)
        if(FLAG_END):
            m_rotation_rd.stop()
            break
            #sleep(60)

# move left wheel
def rg():
    m_rotation_rg = Motor(OUTPUT_B)
    while True:
        m_rotation_rg.on_for_seconds(SpeedRPM(20), 1)
        sleep(1)
        if(FLAG_END):
            m_rotation_rg.stop()
            break
           # sleep(60)

#move touret
def mouvement_rotation():
    m_rotation_verticale = Motor(OUTPUT_C)
    m_rotation_horizontal = Motor(OUTPUT_D)

    state_rotation_g = "off"

    vit_=15
    m_rotation_horizontal.position = 0 # make sure camera is in center

    while True:

        if(state_rotation_g == "off"):
            m_rotation_horizontal.on_for_seconds(SpeedRPM(vit_), 1)
            if(m_rotation_horizontal.position > 135 ):
                state_rotation_g = "on"
                print(state_rotation_g)
        else:
            m_rotation_horizontal.on_for_seconds(SpeedRPM(-vit_), 1)
            if(m_rotation_horizontal.position < -135):
                state_rotation_g = "off"
                print(state_rotation_g)

        sleep(1)
        if(FLAG_END):
            m_rotation_horizontal.stop()
            break
            #sleep(60)

        """
        m_rotation_verticale.on_for_seconds(SpeedDPM(45), 1)
        m_rotation_verticale.on_for_seconds(SpeedDPM(-45), 1)
        """

def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)



if __name__ == "__main__":


    set_font('Lat15-Terminus24x12')

    # definition of threads
    t1 = threading.Thread(target=pixycam)
    t2 = threading.Thread(target=mouvement_rotation)
    t3 = threading.Thread(target=rd)
    t4 = threading.Thread(target=rg)

    #launch of threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()

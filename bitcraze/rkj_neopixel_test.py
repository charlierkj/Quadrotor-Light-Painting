"""
This script does a scripted flight path using the MotionCommander class.
The path is shaped as a Christmas tree.

Connects to the crazyflie at `URI` and runs a
sequence. Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/250K'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def ringOff(scf):
    scf.cf.param.set_value('ring.solidRed', "0")
    scf.cf.param.set_value('ring.solidGreen', "0")
    scf.cf.param.set_value('ring.solidBlue', "0")


def ringGreen(scf):
    scf.cf.param.set_value('ring.solidRed', "0")
    scf.cf.param.set_value('ring.solidGreen', "255")
    scf.cf.param.set_value('ring.solidBlue', "0")


def ringRed(scf):
    scf.cf.param.set_value('ring.solidRed', "255")
    scf.cf.param.set_value('ring.solidGreen', "0")
    scf.cf.param.set_value('ring.solidBlue', "0")


def ringYellow(scf):
    scf.cf.param.set_value('ring.solidRed', "255")
    scf.cf.param.set_value('ring.solidGreen', "255")
    scf.cf.param.set_value('ring.solidBlue', "0")


def ringBlue(scf):
    scf.cf.param.set_value('ring.solidRed', "0")
    scf.cf.param.set_value('ring.solidGreen', "0")
    scf.cf.param.set_value('ring.solidBlue', "255")


def ringLow(scf):
    scf.cf.param.set_value('ring.solidRed', "0")
    scf.cf.param.set_value('ring.solidGreen', "70")
    scf.cf.param.set_value('ring.solidBlue', "0")


def move(mc, scf, x, y, velocity=0.3):
    scale_x = 5
    scale_y = 1.5
    mc.move_distance(x * scale_x, y * scale_y, 0.0, velocity)
    time.sleep(0.5)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created

        scf.cf.param.set_value('ring.effect', "7")
        ringOff(scf)
        mc = MotionCommander(scf)
        mc.take_off(0.1, 100)

        time.sleep(1)


        ringOff(scf)

        ringLow(scf)
        ringRed(scf)
        time.sleep(3)
        ringOff(scf)

        ringLow(scf)
        ringYellow(scf)
        time.sleep(3)
        ringOff(scf)

        ringLow(scf)
        ringBlue(scf)
        time.sleep(3)
        ringOff(scf)

        time.sleep(1)

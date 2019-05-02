import logging
import time
import math

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def position_callback(data, logconf):
    global x,y,z
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']
    print('pos: ({}, {}, {})'.format(x, y, z))


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    # Scan for Crazyflies and use the first one found
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()
    print('Crazyflies found:')
    for i in available:
        print(i[0])

    if len(available) == 0:
        print('No Crazyflies found, cannot run example')
    else:
        lg_pos = LogConfig(name='Position', period_in_ms=500)
        lg_pos.add_variable('kalman.stateX', 'float')
        lg_pos.add_variable('kalman.stateY', 'float')
        lg_pos.add_variable('kalman.stateZ', 'float')

        cf = Crazyflie(rw_cache='./cache')
        with SyncCrazyflie(available[0][0], cf=cf) as scf:
            with SyncLogger(scf, lg_pos) as logger:
                endTime = time.time() + 10

                for log_entry in logger:
                    timestamp = log_entry[0]
                    data = log_entry[1]
                    logconf_name = log_entry[2]

                    position_callback(data, lg_pos)

                    if time.time() > endTime:
                        break

#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory

def LEDoff(allcfs):
    for cf in allcfs.crazyflies:
        cf.setParam('ring/solidRed', 0)
        cf.setParam('ring/solidGreen', 0)
        cf.setParam('ring/solidBlue', 0)


if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    traj1 = uav_trajectory.ColorTrajectory()
    traj1.loadcsv("fei_traj_color.csv")

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):
        for cf in allcfs.crazyflies:
            cf.uploadTrajectory(0, 0, traj1)

        allcfs.takeoff(targetHeight=1.1, duration=2.0)
        timeHelper.sleep(2.5)
        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, 1.1])
            cf.goTo(pos, 0, 2.0)
        timeHelper.sleep(2.5)

        allcfs.startColorTrajectory(traj1, 0, timescale=TIMESCALE)
        #timeHelper.sleep(2.0)
        #allcfs.startColorTrajectory(traj1, 0, timescale=TIMESCALE, reverse=True)
        LEDoff(allcfs)
        timeHelper.sleep(2.0)
        allcfs.land(targetHeight=0.06, duration=2.0)
        timeHelper.sleep(3.0)

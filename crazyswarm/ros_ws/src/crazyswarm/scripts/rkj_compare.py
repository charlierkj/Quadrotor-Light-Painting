#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator

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
    traj1.loadcsv("tx_traj_color.csv")

    TRIALS = 1
    TIMESCALE = 1.0
    for i in range(TRIALS):
        for cf in allcfs.crazyflies:
            cf.uploadTrajectory(0, 0, traj1)

        allcfs.takeoff(targetHeight=0.5, duration=2.0)
        timeHelper.sleep(2.5)
        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, 0.5])
            cf.goTo(pos, 0, 2.0)

        timeHelper.sleep(2.5)
        allcfs.startColorTrajectory(traj1, 0, timescale=TIMESCALE)
        #timeHelper.sleep(2.0)
        #allcfs.startColorTrajectory(traj1, 0, timescale=TIMESCALE, reverse=True)
        LEDoff(allcfs)
        timeHelper.sleep(2.0)
        allcfs.land(targetHeight=0.06, duration=2.0)
        timeHelper.sleep(3.0)
        
        gs = gridspec.GridSpec(3,1)
        fig = plt.figure()
        
        xmajorLocator = MultipleLocator(5)
        xminorLocator = MultipleLocator(1)

        ax0 = plt.subplot(gs[0,0])
        ax0.set_ylabel('X-position')
        ax0.set_xlim([-1, math.ceil(np.array(cf.record)[-1,0] + 1)])
        ax0.xaxis.set_major_locator(xmajorLocator)
        ax0.xaxis.set_minor_locator(xminorLocator)
        ax0.xaxis.grid(True, which='minor')
        ax0.yaxis.grid(True, which='major')

        ax1 = plt.subplot(gs[1,0])
        ax1.set_ylabel('Y-position')
        ax1.set_xlim([-1, math.ceil(np.array(cf.record)[-1,0] + 1)])
        ax1.xaxis.set_major_locator(xmajorLocator)
        ax1.xaxis.set_minor_locator(xminorLocator)
        ax1.xaxis.grid(True, which='minor')
        ax1.yaxis.grid(True, which='major')

        ax2 = plt.subplot(gs[2,0])
        ax2.set_ylabel('Z-position')
        ax2.set_xlim([-1, math.ceil(np.array(cf.record)[-1,0] + 1)])
        ax2.xaxis.set_major_locator(xmajorLocator)
        ax2.xaxis.set_minor_locator(xminorLocator)
        ax2.xaxis.grid(True, which='minor')
        ax2.yaxis.grid(True, which='major')
  
        for cf in allcfs.crazyflies:
            ax0.scatter(np.array(cf.record)[:,0], np.array(cf.record)[:,1], c=np.array(cf.record)[:,4:7]/255, linewidths=0)
            ax1.scatter(np.array(cf.record)[:,0], np.array(cf.record)[:,2], c=np.array(cf.record)[:,4:7]/255, linewidths=0) 
            ax2.scatter(np.array(cf.record)[:,0], np.array(cf.record)[:,3], c=np.array(cf.record)[:,4:7]/255, linewidths=0)
            #np.savetxt("tx_test3.csv", np.array(cf.record), fmt="%.6f", delimiter=",", header="time,X,Y,Z,R,G,B")
                
        plt.show()

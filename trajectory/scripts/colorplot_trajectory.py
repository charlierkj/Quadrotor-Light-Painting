#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import argparse

import uav_trajectory

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("trajectory", type=str, help="CSV file containing trajectory")
  parser.add_argument("--stretchtime", type=float, help="stretch time factor (smaller means faster)")
  args = parser.parse_args()

  traj = uav_trajectory.ColorTrajectory()
  traj.loadcsv(args.trajectory)

  if args.stretchtime:
    traj.stretchtime(args.stretchtime)

  ts = np.arange(0, traj.duration, 0.01)
  evals = np.empty((len(ts), 15))
  seg = np.zeros(len(traj.polynomials))
  for t, i in zip(ts, range(0, len(ts))):
    e = traj.eval(t)
    evals[i, 0:3]  = e.pos
    evals[i, 3:6]  = e.vel
    evals[i, 6:9]  = e.acc
    evals[i, 9:12] = e.omega
    evals[i, 12]   = e.yaw
    evals[i, 13]   = e.roll
    evals[i, 14]   = e.pitch
    seg[traj.segment(t)] = t*100

  velocity = np.linalg.norm(evals[:,3:6], axis=1)
  acceleration = np.linalg.norm(evals[:,6:9], axis=1)
  omega = np.linalg.norm(evals[:,9:12], axis=1)

  # print stats
  print("max speed (m/s): ", np.max(velocity))
  print("max acceleration (m/s^2): ", np.max(acceleration))
  print("max omega (rad/s): ", np.max(omega))
  print("max roll (deg): ", np.max(np.degrees(evals[:,13])))
  print("max pitch (deg): ", np.max(np.degrees(evals[:,14])))

  # Create 3x1 sub plots
  gs = gridspec.GridSpec(6, 1)
  fig = plt.figure()
  
  ax0 = plt.subplot(gs[0:2, 0], projection='3d') # row 0
  ax2 = plt.subplot(gs[2, 0]) # row 2
  ax3 = plt.subplot(gs[3, 0]) # row 3
  ax4 = plt.subplot(gs[4, 0]) # row 4
  ax5 = plt.subplot(gs[5, 0]) # row 5
  # ax6 = plt.subplot(gs[6, 0]) # row 6
  # ax7 = plt.subplot(gs[7, 0]) # row 7
  
  start = 0
  
  for i in range(0,len(seg)):
    end = int(seg[i])
    
    ax0.plot(evals[start:end,0], evals[start:end,1], evals[start:end,2], color=traj.color[i]/255)
    ax0.set_xlim(-0.7, 0.7)
    ax0.axis('equal')

    ax2.plot(ts[start:end], velocity[start:end], color=traj.color[i]/255)
    ax2.set_ylabel("velocity [m/s]")

    ax3.plot(ts[start:end], acceleration[start:end], color=traj.color[i]/255)
    ax3.set_ylabel("acceleration [m/s^2]")

    ax4.plot(ts[start:end], omega[start:end], color=traj.color[i]/255)
    ax4.set_ylabel("omega [rad/s]")

    ax5.plot(ts[start:end], np.degrees(evals[start:end,12]), color=traj.color[i]/255)
    ax5.set_ylabel("yaw [deg]")
    
    # ax6.plot(ts[start:end], np.degrees(evals[start:end,13]), color=traj.color[i]/255)
    # ax6.set_ylabel("roll [deg]")

    # ax7.plot(ts[start:end], np.degrees(evals[start:end,14]), color=traj.color[i]/255)
    # ax7.set_ylabel("pitch [deg]")

    start = end

  plt.show()

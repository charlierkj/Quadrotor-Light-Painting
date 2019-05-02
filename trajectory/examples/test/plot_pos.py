#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import argparse

import uav_trajectory
import math

if __name__ == "__main__":
  traj1 = uav_trajectory.Trajectory()
  traj1.loadcsv('snake_traj.csv')
  
  traj2 = uav_trajectory.Trajectory()
  traj2.loadcsv('snake_n.csv')
   
  traj3 = uav_trajectory.Trajectory()
  traj3.loadcsv('snake_n2.csv')

  t1 = np.arange(0, traj1.duration, 0.01)
  evals1 = np.empty((len(t1), 15))
  for t, i in zip(t1, range(0, len(t1))):
    e = traj1.eval(t)
    evals1[i, 0:3]  = e.pos
    evals1[i, 3:6]  = e.vel
    evals1[i, 6:9]  = e.acc
    evals1[i, 9:12] = e.omega
    evals1[i, 12]   = e.yaw
    evals1[i, 13]   = e.roll
    evals1[i, 14]   = e.pitch

  t2 = np.arange(0, traj2.duration, 0.01)
  evals2 = np.empty((len(t2), 15))
  for t, i in zip(t2, range(0, len(t2))):
    e = traj2.eval(t)
    evals2[i, 0:3]  = e.pos
    evals2[i, 3:6]  = e.vel
    evals2[i, 6:9]  = e.acc
    evals2[i, 9:12] = e.omega
    evals2[i, 12]   = e.yaw
    evals2[i, 13]   = e.roll
    evals2[i, 14]   = e.pitch

  t3 = np.arange(0, traj3.duration, 0.01)
  evals3 = np.empty((len(t3), 15))
  for t, i in zip(t3, range(0, len(t3))):
    e = traj3.eval(t)
    evals3[i, 0:3]  = e.pos
    evals3[i, 3:6]  = e.vel
    evals3[i, 6:9]  = e.acc
    evals3[i, 9:12] = e.omega
    evals3[i, 12]   = e.yaw
    evals3[i, 13]   = e.roll
    evals3[i, 14]   = e.pitch

  velocity1 = np.linalg.norm(evals1[:,3:6], axis=1)
  acceleration1 = np.linalg.norm(evals1[:,6:9], axis=1)
  omega1 = np.linalg.norm(evals1[:,9:12], axis=1)

  velocity2 = np.linalg.norm(evals2[:,3:6], axis=1)
  acceleration2 = np.linalg.norm(evals2[:,6:9], axis=1)
  omega2 = np.linalg.norm(evals2[:,9:12], axis=1)

  velocity3 = np.linalg.norm(evals3[:,3:6], axis=1)
  acceleration3 = np.linalg.norm(evals3[:,6:9], axis=1)
  omega3 = np.linalg.norm(evals3[:,9:12], axis=1)

  wps1 = []
  wps2 = []
  wps3 = []
  t_wps1 = []
  t_wps2 = []
  t_wps3 = []
  wps1.append([0,0,0])
  wps2.append([0,0,0])
  wps3.append([0,0,0])
  t_wps1.append(0)
  t_wps2.append(0)
  t_wps3.append(0)
  t_1 = 0.0
  t_2 = 0.0
  t_3 = 0.0
  for i in range(0, len(traj1.polynomials)):
    t_1 += traj1.durations[i]
    t_2 += traj2.durations[i]
    t_3 += traj3.durations[i]
    t_wps1.append(t_1)
    t_wps2.append(t_2)
    t_wps3.append(t_3)
    wps1.append(traj1.eval(math.floor(t_1*1000)/1000).pos)
    wps2.append(traj2.eval(math.floor(t_2*1000)/1000).pos)
    wps3.append(traj3.eval(math.floor(t_3*1000)/1000).pos)
  wps1 = np.array(wps1)
  t_wps1 = np.array(t_wps1)
  wps2 = np.array(wps2)
  t_wps2 = np.array(t_wps2)  
  wps3 = np.array(wps3)
  t_wps3 = np.array(t_wps3)  
  

  # Create 3x3 sub plots
  gs = gridspec.GridSpec(3, 3)
  fig = plt.figure(figsize=(20,10))

  ax = plt.subplot(gs[0, 0]) # row 0
  ax.plot(t1, evals1[:,0])
  ax.scatter(t_wps1, wps1[:,0], c='r')
  ax.set_title('planar')
  ax.set_ylabel("X position [m]")

  ax = plt.subplot(gs[1, 0]) # row 1
  ax.plot(t1, evals1[:,1])
  ax.scatter(t_wps1, wps1[:,1], c='r')
  ax.set_ylabel("Y position [m]")

  ax = plt.subplot(gs[2, 0]) # row 2
  ax.plot(t1, evals1[:,2])
  ax.scatter(t_wps1, wps1[:,2], c='r')
  ax.set_ylabel("Z position [m]")

  ax = plt.subplot(gs[0, 1]) # row 0
  ax.plot(t2, evals2[:,0])
  ax.scatter(t_wps2, wps2[:,0], c='r')
  ax.set_title('depth range')

  ax = plt.subplot(gs[1, 1]) # row 1
  ax.plot(t2, evals2[:,1])
  ax.scatter(t_wps2, wps2[:,1], c='r')

  ax = plt.subplot(gs[2, 1]) # row 2
  ax.plot(t2, evals2[:,2])
  ax.scatter(t_wps2, wps2[:,2], c='r')

  ax = plt.subplot(gs[0, 2]) # row 0
  ax.plot(t3, evals3[:,0])
  ax.scatter(t_wps3, wps3[:,0], c='r')
  ax.set_title('perturbed planar')

  ax = plt.subplot(gs[1, 2]) # row 1
  ax.plot(t3, evals3[:,1])
  ax.scatter(t_wps3, wps3[:,1], c='r')

  ax = plt.subplot(gs[2, 2]) # row 2
  ax.plot(t3, evals3[:,2])
  ax.scatter(t_wps3, wps3[:,2], c='r')

  plt.show()


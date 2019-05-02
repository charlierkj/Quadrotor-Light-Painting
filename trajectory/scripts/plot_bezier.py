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

  traj = uav_trajectory.BezierTrajectory()
  traj.loadcsv(args.trajectory)

  ts = np.arange(0, traj.duration, 0.01)
  evals = np.empty((len(ts), 3))
  for t, i in zip(ts, range(0, len(ts))):
    evals[i,0:3] = traj.eval(t)

  gs = gridspec.GridSpec(2,1)
  fig = plt.figure()
  ax = plt.subplot(gs[0:2, 0], projection='3d')
  ax.plot(evals[:,0], evals[:,1], evals[:,2])
  ax.set_xlim(-0.7, 0.7)

  plt.show()


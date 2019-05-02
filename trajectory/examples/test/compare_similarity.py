import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

import uav_trajectory
import sys
#sys.setrecursionlimit(10000)

def Transform(x, camera, waypoint):
    new_waypoint = []
    old_x = waypoint[0]
    old_y = waypoint[1]
    old_z = waypoint[2]
    new_x = x
    new_y = (old_y - camera[1])*(new_x - camera[0])/(old_x - camera[0]) + camera[1]
    new_z = (old_z - camera[2])*(new_x - camera[0])/(old_x - camera[0]) + camera[2]
    new_waypoint.append(new_x)
    new_waypoint.append(new_y)
    new_waypoint.append(new_z)
    return np.array(new_waypoint)

def Head(traj):
    traj = np.delete(traj, -1, axis=0)
    return traj

def LCSS(traj1, traj2):
    if len(traj1) == 0 or len(traj2) == 0:
        return 0
    elif abs(traj1[-1,0]-traj2[-1,0]) <= 0.001 and abs(traj1[-1,1]-traj2[-1,1]) <= 0.001:
        return 1 + LCSS(np.delete(traj1, -1, axis=0), np.delete(traj2, -1, axis=0))
    else:
        return max(LCSS(np.delete(traj1, -1, axis=0),traj2), LCSS(traj1,np.delete(traj2, -1, axis=0)))

def Compare_Similarity(traj1, traj2):
    camera = np.array([-2.7686, 0, 0.24828706])
    YZ1 = []
    YZ2 = []
    for t in np.arange(0, traj1.duration, 0.1):
        old_pt = np.array(traj1.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ1.append(new_pt[1:3])
    for t in np.arange(0, traj2.duration, 0.1):
        old_pt = np.array(traj2.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ2.append(new_pt[1:3])
    YZ1 = np.array(YZ1[0:10])
    YZ2 = np.array(YZ2[0:15])
    #plt.plot(YZ1[:,0], YZ1[:,1], c='b')
    #plt.plot(YZ2[:,0], YZ2[:,1], c='r')
    #plt.show()

    return LCSS(YZ1, YZ2)/min(len(YZ1),len(YZ2))
    


if __name__ == "__main__":
    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv('turkey_traj.csv')

    traj2 = uav_trajectory.Trajectory()
    traj2.loadcsv('turkey_n.csv')

    result = Compare_Similarity(traj1, traj2)
    print(result)

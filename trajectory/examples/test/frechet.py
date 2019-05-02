import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

import uav_trajectory
import math


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

def euc_dist(pt1,pt2):
    return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))

def _c(ca,i,j,P,Q):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = euc_dist(P[0],Q[0])
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,P,Q),euc_dist(P[i],Q[0]))
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,P,Q),euc_dist(P[0],Q[j]))
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),euc_dist(P[i],Q[j]))
    else:
        ca[i,j] = float("inf")
    return ca[i,j]

""" Computes the discrete frechet distance between two polygonal lines
Algorithm: http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
P and Q are arrays of 2-element arrays (points)
"""
def frechetDist(P,Q):
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca,-1)
    return _c(ca,len(P)-1,len(Q)-1,P,Q)

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
    YZ1 = np.array(YZ1)
    YZ2 = np.array(YZ2)
    plt.plot(YZ1[:,0], YZ1[:,1], c='b')
    plt.plot(YZ2[:,0], YZ2[:,1], c='r')
    plt.show()
    return frechetDist(YZ1, YZ2)

def Compare_to_Truth(truth_wps, traj1, traj2, traj3):
    camera = np.array([-2.7686, 0, 0.24828706])
    YZ0 = []
    YZ1 = []
    YZ2 = []
    YZ3 = []
    for i in range(0, len(truth_wps)):
        YZ0.append(truth_wps[i,1:3])
    for t in np.arange(0, traj1.duration, 0.1):
        old_pt = np.array(traj1.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ1.append(new_pt[1:3])
    for t in np.arange(0, traj2.duration, 0.1):
        old_pt = np.array(traj2.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ2.append(new_pt[1:3])
    for t in np.arange(0, traj3.duration, 0.1):
        old_pt = np.array(traj3.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ3.append(new_pt[1:3])
    YZ0 = np.array(YZ0)
    YZ1 = np.array(YZ1)
    YZ2 = np.array(YZ2)
    YZ3 = np.array(YZ3)
    result = []
    result.append(frechetDist(YZ0, YZ1))
    result.append(frechetDist(YZ0, YZ2))
    result.append(frechetDist(YZ0, YZ3))
    result = np.array(result)
 
    # Create 3x1 sub plots
    gs = gridspec.GridSpec(3, 1)
    fig = plt.figure()

    ax = plt.subplot(gs[0:2, 0]) # row 0
    ax.plot(-YZ0[:,0], YZ0[:,1], c='r', label='truth')
    ax.plot(-YZ1[:,0], YZ1[:,1], c='b', label='planar')
    ax.plot(-YZ2[:,0], YZ2[:,1], c='y', label='exploit depth 1')
    ax.plot(-YZ3[:,0], YZ3[:,1], c='g', label='exploit depth 2')
    ax.axis('equal')
    plt.legend(loc=1)

    ax = plt.subplot(gs[2, 0]) # row 2
    ax.bar(0, result[0], width = 1, fc = 'b')
    ax.bar(1, result[1], width = 1, fc = 'y')
    ax.bar(2, result[2], width = 1, fc = 'g')
    ax.bar([0,1,2], [0, 0, 0], width=1, tick_label=['planar', 'deep 1', 'deep 2'])
    for i in range(0, len(result)):
        ax.text(i-0.5, result[i]+0.0005, '%s'%float(result[i]))
    ax.set_ylim(0, np.max(result)+0.01)
    ax.set_ylabel("frechet distance[m]")

    plt.show()
    fig.savefig("frechet_snake.pdf", bbox_inches='tight')
    return result
    

if __name__ == "__main__":
    truth_wps = np.loadtxt('snake_truth.csv', delimiter=",")

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv('snake_traj.csv')

    traj2 = uav_trajectory.Trajectory()
    traj2.loadcsv('snake_n.csv')

    traj3 = uav_trajectory.Trajectory()
    traj3.loadcsv('snake_n2.csv')

    result = Compare_to_Truth(truth_wps, traj1, traj2, traj3)
    print(result)


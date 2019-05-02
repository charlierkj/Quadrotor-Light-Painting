import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

import uav_trajectory
import math
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42

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

def Compare_to_Trajectory(traj, pts):
    camera = np.array([-2.7686, 0, 0.24828706])
    YZ1 = []
    YZ2 = []
    for t in np.arange(0, traj.duration, 0.1):
        old_pt = np.array(traj.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ1.append(new_pt[1:3])
    for i in range(0, len(pts)):
        YZ2.append(pts[i,1:3])
    YZ1 = np.array(YZ1)
    YZ2 = np.array(YZ2)
    YZ2[:,0] = -YZ2[:,0]*5472
    YZ2[:,1] = YZ2[:,1]*3648
    ratio_width = (np.max(YZ2[:,0])-np.min(YZ2[:,0]))/(np.max(YZ1[:,0])-np.min(YZ1[:,0]))
    ratio_height = np.max(YZ2[:,1])/np.max(YZ1[:,1])
    ratio = (ratio_width + ratio_height)/2
    YZ2 = YZ2/ratio
    plt.plot(YZ1[:,0], YZ1[:,1], c='b')
    plt.plot(YZ2[:,0], YZ2[:,1], c='r')
    plt.show()
    return frechetDist(YZ1, YZ2)

def Compare(traj1, traj2, traj3, pts1, pts2, pts3):
    camera = np.array([-2.7686, 0, 0.24828706])
    YZ1t = []
    YZ1p = []
    YZ2t = []
    YZ2p = []
    YZ3t = []
    YZ3p = []
    for t in np.arange(0, traj1.duration, 0.1):
        old_pt = np.array(traj1.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ1t.append(new_pt[1:3])
    for i in range(0, len(pts1)):
        YZ1p.append(pts1[i,1:3])
    for t in np.arange(0, traj2.duration, 0.1):
        old_pt = np.array(traj2.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ2t.append(new_pt[1:3])
    for i in range(0, len(pts2)):
        YZ2p.append(pts2[i,1:3])
    for t in np.arange(0, traj3.duration, 0.1):
        old_pt = np.array(traj3.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        YZ3t.append(new_pt[1:3])
    for i in range(0, len(pts3)):
        YZ3p.append(pts3[i,1:3])
    YZ1t = np.array(YZ1t)
    YZ1p = np.array(YZ1p)
    YZ2t = np.array(YZ2t)
    YZ2p = np.array(YZ2p)
    YZ3t = np.array(YZ3t)
    YZ3p = np.array(YZ3p)
    YZ1t[:,0] = -YZ1t[:,0]
    YZ2t[:,0] = -YZ2t[:,0]
    YZ3t[:,0] = -YZ3t[:,0]
    YZ1p[:,0] = YZ1p[:,0]*5472
    YZ2p[:,0] = YZ2p[:,0]*5472
    YZ3p[:,0] = YZ3p[:,0]*5472
    YZ1p[:,1] = YZ1p[:,1]*3648
    YZ2p[:,1] = YZ2p[:,1]*3648
    YZ3p[:,1] = YZ3p[:,1]*3648
    ratio_width = (np.min(YZ1p[:,0])/np.min(YZ1t[:,0])+np.min(YZ2p[:,0])/np.min(YZ1t[:,0])+np.min(YZ3p[:,0])/np.min(YZ3t[:,0]))/3
    ratio_height = (np.max(YZ1p[:,1])/np.max(YZ1t[:,1])+np.max(YZ2p[:,1])/np.max(YZ2t[:,1])+np.max(YZ3p[:,1])/np.max(YZ3t[:,1]))/3
    ratio = (ratio_width + ratio_height)/2
    YZ1p = YZ1p/ratio
    YZ2p = YZ2p/ratio
    YZ3p = YZ3p/ratio
    result = []
    result.append(frechetDist(YZ1t, YZ1p))
    result.append(frechetDist(YZ2t, YZ2p))
    result.append(frechetDist(YZ3t, YZ3p))
    result = np.array(result)
 
    # Create 2x3 sub plots
    gs = gridspec.GridSpec(2, 3)
    fig = plt.figure(figsize=(20,9))

    ax = plt.subplot(gs[0:2, 0]) # row 0, column 0
    ax.plot(YZ1t[:,0], YZ1t[:,1], c='r', label='trajectory')
    ax.plot(YZ1p[:,0], YZ1p[:,1], c='b', label='photo')
    ax.axis('equal')
    ax.set_ylim(-0.1,1)
    ax.tick_params(labelsize=20)
    plt.legend(loc=2, fontsize=20)

    ax = plt.subplot(gs[0:2, 1]) # row 0, column 1
    ax.plot(YZ2t[:,0], YZ2t[:,1], c='r')
    ax.plot(YZ2p[:,0], YZ2p[:,1], c='b')
    ax.axis('equal')
    ax.set_ylim(-0.1,1)
    ax.tick_params(labelsize=20)

    ax = plt.subplot(gs[0:2, 2]) # row 0, column 2
    ax.plot(YZ3t[:,0], YZ3t[:,1], c='r')
    ax.plot(YZ3p[:,0], YZ3p[:,1], c='b')
    ax.axis('equal')
    ax.set_ylim(-0.1,1)
    ax.tick_params(labelsize=20)

    #ax = plt.subplot(gs[2, 0:3]) # row 2
    #ax.bar([0,1,2], result, width=0.8, tick_label=['planar', 'deep 1', 'deep 2'])
    #for i in range(0, len(result)):
    #     ax.text(i-0.4, result[i]+0.0005, '%s'%float(result[i]))
    #ax.set_ylim(0, np.max(result)+0.01)
    #ax.set_ylabel("frechet distance[m]")

    plt.show()
    fig.savefig("frechet3_snake.pdf", bbox_inches='tight')
    return result
    

if __name__ == "__main__":
    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv('snake_traj.csv')
    traj2 = uav_trajectory.Trajectory()
    traj2.loadcsv('snake_n.csv')
    traj3 = uav_trajectory.Trajectory()
    traj3.loadcsv('snake_n2.csv')

    pts1 = np.loadtxt('snake_planar.csv', delimiter=",")
    pts2 = np.loadtxt('snake_deep1.csv', delimiter=",")
    pts3 = np.loadtxt('snake_deep2.csv', delimiter=",")
    
    result = Compare(traj1, traj2, traj3, pts1, pts2, pts3)
    print(result)


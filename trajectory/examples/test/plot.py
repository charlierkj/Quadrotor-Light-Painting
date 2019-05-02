import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator

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

def Plot(traj1, traj2, traj3, wps1, wps2, wps3):
    camera = np.array([-2.7686, 0, 0.24828706])
    P1_3d = []
    P1_2d = []
    P2_3d = []
    P2_2d = []
    P3_3d = []
    P3_2d = []
    for t in np.arange(0, traj1.duration, 0.01):
        old_pt = np.array(traj1.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        P1_3d.append(old_pt)
        P1_2d.append(new_pt)
    for t in np.arange(0, traj2.duration, 0.01):
        old_pt = np.array(traj2.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        P2_3d.append(old_pt)
        P2_2d.append(new_pt)
    for t in np.arange(0, traj3.duration, 0.01):
        old_pt = np.array(traj3.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        P3_3d.append(old_pt)
        P3_2d.append(new_pt)
    P1_3d = np.array(P1_3d)
    P1_2d = np.array(P1_2d)
    P2_3d = np.array(P2_3d)
    P2_2d = np.array(P2_2d)
    P3_3d = np.array(P3_3d)
    P3_2d = np.array(P3_2d)
    print(np.max(P2_3d[:,0]))
    print(np.min(P2_3d[:,0]))
    print(np.max(P3_3d[:,0]))
    print(np.min(P3_3d[:,0]))
 
    # Create 2x3 sub plots
    gs = gridspec.GridSpec(2, 3)
    fig = plt.figure(figsize=(20,10))

    ax = plt.subplot(gs[0, 0], projection='3d') # row 0, column 0
    ax.plot(-P1_3d[:,0], -P1_3d[:,1], P1_3d[:,2])
    ax.scatter(-wps1[:,0], -wps1[:,1], wps1[:,2], c='r')
    ax.axis('equal')
    ax.set_xlim(-0.8,0.4)
    ax.set_ylim(-0.5,0.5)
    ax.set_zlim(0,0.8)
    ax.xaxis.set_major_locator(MultipleLocator(0.3))
    ax.yaxis.set_major_locator(MultipleLocator(0.3))
    ax.tick_params(labelsize=20)

    ax = plt.subplot(gs[1, 0]) # row 1, column 0
    ax.plot(-P1_2d[:,1], P1_2d[:,2])
    ax.scatter(-wps1[:,1], wps1[:,2], c='r')
    ax.axis('equal')
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.tick_params(labelsize=20)

    ax = plt.subplot(gs[0, 1], projection='3d') # row 0, column 1
    ax.plot(-P2_3d[:,0], -P2_3d[:,1], P2_3d[:,2])
    ax.scatter(-wps2[:,0], -wps2[:,1], wps2[:,2], c='r')
    ax.axis('equal')
    ax.set_xlim(-0.8,0.4)
    ax.set_ylim(-0.5,0.5)
    ax.set_zlim(0,0.8)
    ax.xaxis.set_major_locator(MultipleLocator(0.3))
    ax.yaxis.set_major_locator(MultipleLocator(0.3))
    ax.tick_params(labelsize=20)

    ax = plt.subplot(gs[1, 1]) # row 1, column 1
    ax.plot(-P2_2d[:,1], P2_2d[:,2])
    ax.scatter(-wps1[:,1], wps1[:,2], c='r')
    ax.axis('equal')
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.tick_params(labelsize=20)

    ax = plt.subplot(gs[0, 2], projection='3d') # row 0, column 2
    ax.plot(-P3_3d[:,0], -P3_3d[:,1], P3_3d[:,2])
    ax.scatter(-wps3[:,0], -wps3[:,1], wps3[:,2], c='r')
    ax.axis('equal')
    ax.set_xlim(-0.8,0.4)
    ax.set_ylim(-0.5,0.5)
    ax.set_zlim(0,0.8)
    ax.xaxis.set_major_locator(MultipleLocator(0.3))
    ax.yaxis.set_major_locator(MultipleLocator(0.3))
    ax.tick_params(labelsize=20)

    ax = plt.subplot(gs[1, 2]) # row 1, column 2
    ax.plot(-P3_2d[:,1], P3_2d[:,2])
    ax.scatter(-wps1[:,1], wps1[:,2], c='r')
    ax.axis('equal')
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.tick_params(labelsize=20)
    
    plt.show()
    fig.savefig("plot_snake.pdf", bbox_inches='tight')
    

if __name__ == "__main__":
    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv('snake_traj.csv')

    traj2 = uav_trajectory.Trajectory()
    traj2.loadcsv('snake_n.csv')

    traj3 = uav_trajectory.Trajectory()
    traj3.loadcsv('snake_n2.csv')

    wps1 = np.loadtxt('snake_wps.csv', delimiter=",")

    wps2 = np.loadtxt('snake_wps_depth.csv', delimiter=",")
 
    wps3 = np.loadtxt('snake_wps_depth2.csv', delimiter=",")

    Plot(traj1, traj2, traj3, wps1, wps2, wps3)

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

def Plot(traj1, traj2, traj3):
    camera = np.array([-2.7686, 0, 0.24828706-0.5])
    P1_3d = []
    P1_2d = []
    P2_3d = []
    P2_2d = []
    P3_3d = []
    P3_2d = []
    seg1 = np.zeros(len(traj1.polynomials)) 
    seg2 = np.zeros(len(traj2.polynomials)) 
    seg3 = np.zeros(len(traj3.polynomials)) 
    for t in np.arange(0, traj1.duration, 0.01):
        old_pt = np.array(traj1.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        P1_3d.append(old_pt)
        P1_2d.append(new_pt)
        seg1[traj1.segment(t)] = t*100
    for t in np.arange(0, traj2.duration, 0.01):
        old_pt = np.array(traj2.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        P2_3d.append(old_pt)
        P2_2d.append(new_pt)
        seg2[traj2.segment(t)] = t*100
    for t in np.arange(0, traj3.duration, 0.01):
        old_pt = np.array(traj3.eval(t).pos)
        new_pt = Transform(0, camera, old_pt)
        P3_3d.append(old_pt)
        P3_2d.append(new_pt)
        seg3[traj3.segment(t)] = t*100
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

    ax00 = plt.subplot(gs[0, 0], projection='3d') # row 0, column 0
    ax10 = plt.subplot(gs[1, 0]) # row 1, column 0
    ax01 = plt.subplot(gs[0, 1], projection='3d') # row 0, column 1
    ax11 = plt.subplot(gs[1, 1]) # row 1, column 1
    ax02 = plt.subplot(gs[0, 2], projection='3d') # row 0, column 2
    ax12 = plt.subplot(gs[1, 2]) # row 1, column 2

    start = 0
    for i in range(0,len(seg1)): 
        end = int(seg1[i])
        ax00.plot(-P1_3d[start:end,0], -P1_3d[start:end,1], P1_3d[start:end,2], c=traj1.color[i]/255)
        ax00.axis('equal')
        ax00.set_xlim(-0.8,0.4)
        ax00.set_ylim(-0.5,0.5)
        ax00.set_zlim(0,0.8)
        ax00.xaxis.set_major_locator(MultipleLocator(0.3))
        ax00.yaxis.set_major_locator(MultipleLocator(0.3))
        ax00.tick_params(labelsize=20)

        ax10.plot(-P1_2d[start:end,1], P1_2d[start:end,2], c=traj1.color[i]/255)
        ax10.axis('equal')
        ax10.xaxis.set_major_locator(MultipleLocator(0.2))
        ax10.yaxis.set_major_locator(MultipleLocator(0.2))
        ax10.tick_params(labelsize=20)
        start = end
    
    start = 0
    for i in range(0,len(seg2)): 
        end = int(seg2[i])
        ax01.plot(-P2_3d[start:end,0], -P2_3d[start:end,1], P2_3d[start:end,2], color=traj2.color[i]/255)
        ax01.axis('equal')
        ax01.set_xlim(-0.8,0.4)
        ax01.set_ylim(-0.5,0.5)
        ax01.set_zlim(0,0.8)
        ax01.xaxis.set_major_locator(MultipleLocator(0.3))
        ax01.yaxis.set_major_locator(MultipleLocator(0.3))
        ax01.tick_params(labelsize=20)
    
        ax11.plot(-P2_2d[start:end,1], P2_2d[start:end,2], color=traj2.color[i]/255)
        ax11.axis('equal')
        ax11.xaxis.set_major_locator(MultipleLocator(0.2))
        ax11.yaxis.set_major_locator(MultipleLocator(0.2))
        ax11.tick_params(labelsize=20)
        start = end
   
    start = 0
    for i in range(0,len(seg3)):
        end = int(seg3[i])
        ax02.plot(-P3_3d[start:end,0], -P3_3d[start:end,1], P3_3d[start:end,2], color=traj3.color[i]/255)
        ax02.axis('equal')
        ax02.set_xlim(-0.8,0.4)
        ax02.set_ylim(-0.5,0.5)
        ax02.set_zlim(0,0.8)
        ax02.xaxis.set_major_locator(MultipleLocator(0.3))
        ax02.yaxis.set_major_locator(MultipleLocator(0.3))
        ax02.tick_params(labelsize=20)
     
        ax12.plot(-P3_2d[start:end,1], P3_2d[start:end,2], c=traj3.color[i]/255)
        ax12.axis('equal')
        ax12.xaxis.set_major_locator(MultipleLocator(0.2))
        ax12.yaxis.set_major_locator(MultipleLocator(0.2))
        ax12.tick_params(labelsize=20)
        start = end
    
    plt.show()
    #fig.savefig("plot_skeleton.pdf", bbox_inches='tight')
    

if __name__ == "__main__":
    traj1 = uav_trajectory.ColorTrajectory()
    traj1.loadcsv('skeleton_traj.csv')

    traj2 = uav_trajectory.ColorTrajectory()
    traj2.loadcsv('skeleton_n.csv')

    traj3 = uav_trajectory.ColorTrajectory()
    traj3.loadcsv('skeleton_n2.csv')

    Plot(traj1, traj2, traj3)

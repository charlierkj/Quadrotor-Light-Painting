import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

import uav_trajectory
import math


if __name__ == "__main__":
    filename = []
    for i in range(1, 34):
        flnm = str(i)+".csv"
        filename.append(flnm)
    
    
    X = []
    x = 0.0
    traj_set = []
    for i in range(0, len(filename)):
        X.append(x)
        traj = uav_trajectory.Trajectory()
        traj.loadcsv(filename[i])
        traj_set.append(traj)
        x += 0.1
        
    X = np.array(X)
    
    result = []
    distance = []
    for traj in traj_set:
        for i in range(0, len(traj.polynomials)):
            snap_square = 0.0
            if i == 0:
                t0 = 0.0
            else:
                t0 = np.sum(traj.durations[0:i])
            te = np.sum(traj.durations[0:i+1])
            vector = traj.eval(math.floor(te*1000)/1000).pos - traj.eval(math.floor(t0*1000)/1000).pos
            print(vector)
            dstc = np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
            for t in np.arange(t0, te, 0.01):
                snap = traj.eval(t).snap
                snap_square += (snap[0]**2 + snap[1]**2 + snap[2]**2)*0.01
            result.append(snap_square/100000)
            distance.append(dstc)

    result = np.array(result)
    distance = np.array(distance)

    # Create 1x1 sub plots
    gs = gridspec.GridSpec(1, 1)
    fig = plt.figure()
    
    ax = plt.subplot(gs[0, 0]) # row 0
    ax.scatter(distance[:], result[:], c = 'b')
    ax.set_xlabel("distance[m]")
    ax.set_ylabel("integral(snap^2)[x100000]")

    plt.show()
    fig.savefig("snap_distance.pdf", bbox_inches='tight')

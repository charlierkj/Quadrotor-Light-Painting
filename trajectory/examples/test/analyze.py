import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

import uav_trajectory


if __name__ == "__main__":
    filename = []
    filename.append("turkey_0.0_traj.csv")
    filename.append("turkey_0.1_traj.csv")
    filename.append("turkey_0.2_traj.csv")
    filename.append("turkey_0.3_traj.csv")
    filename.append("turkey_0.4_traj.csv")
    filename.append("turkey_0.5_traj.csv")
    filename.append("turkey_0.6_traj.csv")
    filename.append("turkey_0.7_traj.csv")
    filename.append("turkey_0.8_traj.csv")
    filename.append("turkey_0.9_traj.csv")
    filename.append("turkey_1.0_traj.csv")
    filename.append("turkey_n.csv")

    
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
    for traj in traj_set:
        snap_square = 0.0
        for t in np.arange(0, traj.duration, 0.01):
            snap = traj.eval(t).snap
            snap_square += (snap[0]**2 + snap[1]**2 + snap[2]**2)*0.01
        result.append(snap_square)

    result = np.array(result)

    # Create 1x1 sub plots
    gs = gridspec.GridSpec(1, 1)
    fig = plt.figure()
    
    ax = plt.subplot(gs[0, 0]) # row 0
    ax.scatter(X[:], result[:], c = 'b')
    ax.set_xlabel("X_range[m]")
    ax.set_ylabel("integral(snap^2)/duration")

    plt.show()

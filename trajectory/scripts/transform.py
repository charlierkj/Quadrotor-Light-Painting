import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

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

if __name__ == "__main__":
    camera = np.array([-2, 0, 1.2])
    waypoint = np.array([0, 0.5, 1.3])
    new_waypoint = Transform(0.5, camera, waypoint)

    pl = []
    pl.append(camera)
    pl.append(waypoint)
    pl.append(new_waypoint)
    pl = np.array(pl)
    print(pl)
    
    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
  
    ax = plt.subplot(gs[0:2, 0:2], projection='3d') # row 0

    ax.scatter(pl[:,0], pl[:,1], pl[:,2], c = 'r')
    ax.plot(pl[:,0], pl[:,1], pl[:,2], c = 'b')

    plt.show()

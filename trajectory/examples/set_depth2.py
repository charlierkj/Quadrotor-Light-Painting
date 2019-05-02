import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import argparse


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

def Set_Depth(wpsfile):
    camera = np.array([-2.7686, 0, 0.24828706-0.5])
    wps = np.loadtxt(wpsfile, delimiter=",")
    new_wps = []
    X = []
    for i in range(0, len(wps)):
        if i == 0:
            x = 0
        else:
            vector = wps[i] - wps[i-1]
            distance = np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
            if distance >= 0.2:
                x = X[i-1]
            else:
                delta_x = np.sqrt(0.25**2 - distance**2)
                if X[i-1] <= 0:
                    x = X[i-1] + delta_x
                else:
                    x = X[i-1] - delta_x
        X.append(x)
        
    for i in range(0, len(X)):
        new_wps.append(Transform(X[i], camera, wps[i]))
    return np.array(new_wps)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="set depth for waypoints")
    parser.add_argument("inputfile", help="input file destination")
    parser.add_argument("outputfile", help="output file destination")
    args = parser.parse_args()

    inputfile = args.inputfile
    outputfile = args.outputfile
    
    new_wps = Set_Depth(inputfile)
    np.savetxt(outputfile, new_wps, fmt="%.6f", delimiter=",")

    # Create 2x2 sub plots
    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()

    ax = plt.subplot(gs[0:2, 0:2], projection='3d') # row 0
    ax.plot(new_wps[:,0], new_wps[:,1], new_wps[:,2])
    ax.scatter(new_wps[:,0], new_wps[:,1], new_wps[:,2], c='r')

    plt.show()   

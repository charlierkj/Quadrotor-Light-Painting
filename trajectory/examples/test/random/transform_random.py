import numpy as np
import random


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

def Transform_Random(rg, wpsfile):
    camera = np.array([-2.7686, 0, 0.24828706])
    wps = np.loadtxt(wpsfile, delimiter=",")
    new_wps = []
    for i in range(0, len(wps)):          
        waypoint = np.array(wps[i,:])
        if i == 0:
            x = 0
        else:
            x = random.random()
            x = x -0.3
            x *= rg
        new_wps.append(Transform(x, camera, waypoint))
    return np.array(new_wps)
    

if __name__ == "__main__":
    filename = []
    filename.append("turkey_0.0_wps.csv")
    filename.append("turkey_0.1_wps.csv")
    filename.append("turkey_0.2_wps.csv")
    filename.append("turkey_0.3_wps.csv")
    filename.append("turkey_0.4_wps.csv")
    filename.append("turkey_0.5_wps.csv")
    filename.append("turkey_0.6_wps.csv")
    filename.append("turkey_0.7_wps.csv")
    filename.append("turkey_0.8_wps.csv")
    filename.append("turkey_0.9_wps.csv")
    filename.append("turkey_1.0_wps.csv")
    
    rng = 0.0
    for i in range(0, len(filename)):
        new_wps = Transform_Random(rng, "turkey_wps.csv")
        np.savetxt(filename[i], new_wps, fmt="%.6f", delimiter=",")
        rng += 0.1
        
                   
    
    

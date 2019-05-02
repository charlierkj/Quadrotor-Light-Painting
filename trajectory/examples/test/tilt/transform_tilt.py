import numpy as np


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

def Transform_Tilt(x, wpsfile):
    camera = np.array([-2, 0, 1.2])
    wps = np.loadtxt(wpsfile, delimiter=",")
    max_z = np.max(wps[:,2])
    new_wps = []
    for row in wps:
        waypoint = np.array(row)
        new_x = (x/max_z)*waypoint[2]
        new_wps.append(Transform(new_x, camera, waypoint))
    return np.array(new_wps)
    

if __name__ == "__main__":
    filename = []
    filename.append("camel1_-0.3_wps.csv")
    filename.append("camel1_-0.2_wps.csv")
    filename.append("camel1_-0.1_wps.csv")
    filename.append("camel1_0.0_wps.csv")
    filename.append("camel1_0.1_wps.csv")
    filename.append("camel1_0.2_wps.csv")
    filename.append("camel1_0.3_wps.csv")
    filename.append("camel1_0.4_wps.csv")
    filename.append("camel1_0.5_wps.csv")
    filename.append("camel1_0.6_wps.csv")
    filename.append("camel1_0.7_wps.csv")
    
    x = -0.3
    for i in range(0, len(filename)):
        new_wps = Transform_Tilt(x, "camel1_wps.csv")
        np.savetxt(filename[i], new_wps, fmt="%.6f", delimiter=",")
        x += 0.1
        
                   
    
    

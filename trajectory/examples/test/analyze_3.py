import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

import uav_trajectory
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42


if __name__ == "__main__":
    filename = []
    filename.append("camel1_traj.csv")
    filename.append("camel1_n.csv")
    filename.append("camel1_n2.csv")

    #filename.append("dog_traj.csv")
    #filename.append("dog_n.csv")
    #filename.append("dog_n2.csv")

    filename.append("elephant_traj.csv")
    filename.append("elephant_n.csv")
    filename.append("elephant_n2.csv")

    filename.append("fox_traj.csv")
    filename.append("fox_n.csv")
    filename.append("fox_n2.csv")
    
    filename.append("frog_traj.csv")
    filename.append("frog_n.csv")
    filename.append("frog_n2.csv")
    
    filename.append("kangroo_traj.csv")
    filename.append("kangroo_n.csv")
    filename.append("kangroo_n2.csv")

    filename.append("penguin_traj.csv")
    filename.append("penguin_n.csv")
    filename.append("penguin_n2.csv")

    filename.append("reindeer_traj.csv")
    filename.append("reindeer_n.csv")
    filename.append("reindeer_n2.csv")

    filename.append("snake_traj.csv")
    filename.append("snake_n.csv")
    filename.append("snake_n2.csv")

    filename.append("squirrel_traj.csv")
    filename.append("squirrel_n.csv")
    filename.append("squirrel_n2.csv")

    filename.append("turkey_traj.csv")
    filename.append("turkey_n.csv")
    filename.append("turkey_n2.csv")

    #filename.append("fei_traj.csv")
    #filename.append("fei_n.csv")
    #filename.append("fei_n2.csv")

    traj_set = []
    for i in range(0, len(filename)):
        traj = uav_trajectory.Trajectory()
        traj.loadcsv(filename[i])
        traj_set.append(traj)
    
    
    result = []    
    for traj in traj_set:
        snap_square = 0.0
        for t in np.arange(0, traj.duration, 0.01):
            snap = traj.eval(t).snap
            snap_square += (snap[0]**2 + snap[1]**2 + snap[2]**2)*0.01
        result.append(snap_square/traj.duration)

    result = np.array(result)/1000

    name_list = ['camel', 'elephant', 'fox', 'cheetah', 'kangroo', 'penguin', 'reindeer', 'snake', 'squirrel', 'flamingo']
    original = []
    new1 = []
    new2 = []
    for i in range(0, int(len(result)/3)):
        original.append(result[3*i])
        new1.append(result[3*i+1])
        new2.append(result[3*i+2])
    original = np.array(original)
    new1 = np.array(new1)
    new2 = np.array(new2)

    # Create bar plots
    x = list(range(len(original)))
    total_width, n = 0.75, 3
    width = total_width/n
    fig = plt.figure(figsize=(20,10))
    
    plt.bar(x, original, width = width, label = 'planar', fc = 'b')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, new1, width = width, label = 'depth range', fc = 'g')
    plt.xticks(x, name_list, rotation=90, fontsize=20)
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, new2, width = width, label = 'perturbed planar', fc = 'r')
    
    #for i in range(len(x)):
    #    x[i] = x[i] - width/2
    #plt.bar(x, np.zeros(len(new)), tick_label = name_list)
    
    plt.tick_params(labelsize=30)
    plt.legend(loc=1, fontsize=30)
    plt.ylabel('integral snap squared over duration [x1000]', fontsize=30) 
    
    plt.show()
    fig.savefig("snap_over_duration.pdf", bbox_inches='tight')

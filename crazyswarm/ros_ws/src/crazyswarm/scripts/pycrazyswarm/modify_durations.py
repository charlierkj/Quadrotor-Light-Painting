import math
import numpy as np

def Compute_Error(traj):
    error = []
    for trj in traj:
        err = 0.16076094185108203 + 1.3664037055584255*trj[0] + 0.5208754188621872*trj[1]
        error.append(err)
    error = np.array(error)
    return error

def Compute_Clr_Time(traj):
    clr_time = []
    for trj in traj:
        ct= 0.34642245879716294 + 2.5433148927326727*trj[0] + 0.9512002284249617*trj[1]
        clr_time.append(ct)
    clr_time = np.array(clr_time)
    return clr_time

def Convert_to_Exp_Time(color_time):
    exp_time = -0.027539963140963852 + 0.46980759711901743*color_time
    return np.array(exp_time)

def Convert_to_True_Time(exp_time):
    true_time = 0.11047499026072671 + 0.9449629391746918*exp_time
    return np.array(true_time)

def Modify_Durations(trajectory):
    traj = []
    for i in range(0, len(trajectory.polynomials)-1):
        trj = []
        distance = math.sqrt((trajectory.polynomials[i+1].px.p[0]-trajectory.polynomials[i].px.p[0])**2+(trajectory.polynomials[i+1].py.p[0]-trajectory.polynomials[i].py.p[0])**2+(trajectory.polynomials[i+1].pz.p[0]-trajectory.polynomials[i].pz.p[0])**2)
        trj.append(distance)
        trj.append(trajectory.durations[i])
        traj.append(trj)
    trj = []
    distance = math.sqrt(trajectory.polynomials[-1].px.p[0]**2+trajectory.polynomials[-1].py.p[0]**2+trajectory.polynomials[-1].pz.p[0]**2)
    trj.append(distance)
    trj.append(trajectory.durations[-1])
    traj.append(trj)
    traj = np.array(traj)
    traj[:,0] = np.sqrt(traj[:,0])

    error = Compute_Error(traj)
    clr_time = Compute_Clr_Time(traj)
    durations = clr_time - error
    durations = Convert_to_Exp_Time(durations)

    ratio = np.sum(0.10933480847732813 + 2.1021489809018195*durations)/np.sum(Convert_to_True_Time(trajectory.durations))
    print(ratio)
    durations = durations/ratio
    return durations

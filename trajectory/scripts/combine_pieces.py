#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import argparse
import uav_trajectory
import cvxopt
from cvxopt import matrix


def Generate_P(times, dt, u):
    P1 = np.zeros((8, 8))
    duration = times[-1]
    for t in np.arange(0, duration, dt):
        p1 = np.array([0., 0., 0., 0., 24., 120*t, 360*t**2, 840*t**3]).reshape((1,8))
        P1 += np.dot(p1.T, p1)*dt

    P2 = np.zeros((8,8))
    for i in range(0, len(times)-1):
        t = times[i]
        p2 = np.array([1., t, t**2, t**3, t**4, t**5, t**6, t**7]).reshape((1,8))
        P2 += np.dot(p2.T, p2)
        
    P = 2*(P1*u + P2)
    return matrix(P)

def Generate_q(times, waypoints):
    q = np.zeros((8,1))
    for i in range(0, len(times)-1):
        t = times[i]
        pos = waypoints[i]
        q += (-2)*pos*np.array([1., t, t**2, t**3, t**4, t**5, t**6, t**7]).reshape((8,1))
    return matrix(q)

def Generate_A(duration):
    t0 = 0
    te = duration
    A = np.array([[1., t0, t0**2, t0**3, t0**4, t0**5, t0**6, t0**7],
                  [0., 1., 2*t0, 3*t0**2, 4*t0**3, 5*t0**4, 6*t0**5, 7*t0**6],
                  [0., 0., 2., 6*t0, 12*t0**2, 20*t0**3, 30*t0**4, 42*t0**5],
                  #[0., 0., 0., 6., 24*t0, 60*t0**2, 120*t0**3, 210*t0**4],
                  [1., te, te**2, te**3, te**4, te**5, te**6, te**7],
                  [0., 1., 2*te, 3*te**2, 4*te**3, 5*te**4, 6*te**5, 7*te**6],
                  [0., 0., 2., 6*te, 12*te**2, 20*te**3, 30*te**4, 42*te**5]])
                  #[0., 0., 0., 6., 24*te, 60*te**2, 120*te**3, 210*te**4]])
    return matrix(A)

def Generate_b(start, end):
    b = np.array([start[0], start[1], start[2], end[0], end[1], end[2]]).reshape((6,1))
    return matrix(b)

def Combine_Pieces(trajectory, p0, pt):
    result = []
    dt = 0.01
    u = 0.0003
    times = []
    waypoints = []
    start = []
    end = []
    t0 = 0.0
    for i in range(p0, pt):
        wp = []
        wp.append(trajectory.polynomials[i+1].px.p[0])
        wp.append(trajectory.polynomials[i+1].py.p[0])
        wp.append(trajectory.polynomials[i+1].pz.p[0])
        waypoints.append(wp)
        times.append(float(t0+trajectory.durations[i]))
        t0 += trajectory.durations[i]
    times = np.array(times)
    waypoints = np.array(waypoints)

    start_time = np.sum(trajectory.durations[0:p0])
    end_time = np.sum(trajectory.durations[0:pt])
    e0 = trajectory.eval(start_time)
    et = trajectory.eval(end_time)

    start.append(e0.pos)
    start.append(e0.vel)
    start.append(e0.acc)
    start.append(e0.jerk)
    end.append(et.pos)
    end.append(et.vel)
    end.append(et.acc)
    end.append(et.jerk)

    start = np.array(start)
    end = np.array(end)

    duration = times[-1]
    
    for i in range(0, 3):
        P = Generate_P(times, dt, u)
        q = Generate_q(times, waypoints[:,i])
        A = Generate_A(duration)
        b = Generate_b(start[:,i], end[:,i])
        sol = cvxopt.solvers.qp(P=P, q=q, G=None, h=None, A=A, b=b, kktsolver='ldl')
        result.append(np.array(sol['x']).reshape((8,)))

    return np.array(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("trajectory", type=str, help="CSV file containing trajectory")
    parser.add_argument("--stretchtime", type=float, help="stretch time factor (smaller means faster)")
    args = parser.parse_args()

    traj = uav_trajectory.ColorTrajectory()
    traj.loadcsv(args.trajectory)

    p0 = 0
    pt = 3

    result = Combine_Pieces(traj, p0, pt)
    print(result)

    points = []
    for i in range(p0, pt+1):
        p = []
        p.append(traj.polynomials[i].px.p[0])
        p.append(traj.polynomials[i].py.p[0])
        p.append(traj.polynomials[i].pz.p[0])
        points.append(p)
    points = np.array(points)

    X = []
    Y = []
    Z = []
    duration = np.sum(traj.durations[p0:pt])
    for t in np.arange(0.0, duration, 0.01):
        T = np.array([1., t, t**2, t**3, t**4, t**5, t**6, t**7]).reshape((8,1))
        X.append(np.dot(result[0,:], T))
        Y.append(np.dot(result[1,:], T))
        Z.append(np.dot(result[2,:], T))
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
        

    # Create 2x2 sub plots
    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
  
    ax = plt.subplot(gs[0:2, 0:2], projection='3d') # row 0

    ax.scatter(points[:,0], points[:,1], points[:,2], c = 'r')
    ax.plot(X[:,0], Y[:,0], Z[:,0], c = 'b')

    plt.show()

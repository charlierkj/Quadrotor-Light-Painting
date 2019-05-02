#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import argparse
import csv
import math


def Scale(x):
    maximum = np.max(x)
    minimum = np.min(x)
    mean = np.mean(x)
    return (x-mean)/(maximum-minimum)

def Eval_H(theta0, theta1, theta2, x1, x2):
    H = theta0 + theta1*x1 + theta2*x2
    return H

def Cost_Function(theta0, theta1, theta2, X):
    J = 0
    m = len(X)
    for x in X:
        J += ((theta0+theta1*x[1]+theta2*x[2])-x[0])**2
    J *= 1/(2*m) 
    return J

def Diff_Cost(theta0, theta1, theta2, X):
    diffJ = []
    diffJ0 = 0
    diffJ1 = 0
    diffJ2 = 0
    for x in X:
        diffJ0 += (Eval_H(theta0, theta1, theta2, x[1], x[2])-x[0])
        diffJ1 += (Eval_H(theta0, theta1, theta2, x[1], x[2])-x[0])*x[1]
        diffJ2 += (Eval_H(theta0, theta1, theta2, x[1], x[2])-x[0])*x[2]
    diffJ.append(diffJ0)
    diffJ.append(diffJ1)
    diffJ.append(diffJ2)
    return np.array(diffJ)
        
def Linear_Regression(X, alpha, epsilon):
    maximum1 = np.max(X[:,1])
    minimum1 = np.min(X[:,1])
    mean1 = np.mean(X[:,1])
    maximum2 = np.max(X[:,2])
    minimum2 = np.min(X[:,2])
    mean2 = np.mean(X[:,2])
    X[:,1] = Scale(X[:,1])
    X[:,2] = Scale(X[:,2])
    theta = []
    theta0 = 0
    theta1 = 0
    theta2 = 0
    error0 = 0
    error1 = Cost_Function(theta0, theta1, theta2, X)
    while abs(error1 - error0) > epsilon:
        temp0 = theta0 - alpha*Diff_Cost(theta0, theta1, theta2, X)[0]
        temp1 = theta1 - alpha*Diff_Cost(theta0, theta1, theta2, X)[1]
        temp2 = theta2 - alpha*Diff_Cost(theta0, theta1, theta2, X)[2]
        theta0 = temp0
        theta1 = temp1
        theta2 = temp2
        error0 = error1
        error1 = Cost_Function(theta0, theta1, theta2, X)
    theta0 = theta0 - theta1*mean1/(maximum1-minimum1) - theta2*mean2/(maximum2-minimum2)
    theta1 = theta1/(maximum1-minimum1)
    theta2 = theta2/(maximum2-minimum2)
    theta.append(theta0)
    theta.append(theta1)
    theta.append(theta2)
    return np.array(theta)
    

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="linear regression and plot")
  parser.add_argument("inputfile", help="input file destination")
  args = parser.parse_args()

  inputfile = args.inputfile
  
  summary = []

  with open(inputfile, 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
          summary.append(row)

  summary = summary[1:]
  summ = []
  for s in summary:
      sm = []
      for se in s:
          sm.append(float(se))
      summ.append(sm)
      
  summ = np.array(summ)

  alpha = 0.01
  epsilon = 0.0001
  
  X = []
  for s in summ:
      x = []
      x.append(s[3])
      x.append(np.sqrt(s[0]))
      x.append(s[1])
      X.append(x)
      
  X = np.array(X)
  
  theta_clr = Linear_Regression(X, alpha, epsilon)
  estm_clr_time = []
  for s in summ:
      estm_clr_time.append(Eval_H(theta_clr[0], theta_clr[1], theta_clr[2], np.sqrt(s[0]), s[1]))
  estm_clr_time = np.array(estm_clr_time)
  
  print("to estimate color_time from distance^0.5 and exp_time")
  print("theta0 = ", theta_clr[0])
  print("theta1 = ", theta_clr[1])
  print("theta2 = ", theta_clr[2])
  print("\n")

  Y = []
  for s in summ:
      y = []
      y.append(s[3]-s[2])
      y.append(np.sqrt(s[0]))
      y.append(s[1])
      Y.append(y)
      
  Y = np.array(Y)

  theta_err = Linear_Regression(Y, alpha, epsilon)
  estm_error = []
  for s in summ:
      estm_error.append(Eval_H(theta_err[0], theta_err[1], theta_err[2], np.sqrt(s[0]), s[1]))
  estm_error = np.array(estm_error)
  
  print("to estimate error from distance^0.5 and exp_time")
  print("theta0 = ", theta_err[0])
  print("theta1 = ", theta_err[1])
  print("theta2 = ", theta_err[2])


  # Create 2x2 sub plots
  gs = gridspec.GridSpec(2, 2)
  fig = plt.figure()

  ax = plt.subplot(gs[0, 0]) # row 0, column 0
  ax.scatter(np.sqrt(summ[:,0]), X[:,0], marker="+", s=30, label="truth")
  ax.scatter(np.sqrt(summ[:,0]), estm_clr_time[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("color_time(s)")
  ax.set_xlabel("distance^0.5(m^0.5)")

  ax = plt.subplot(gs[1, 0]) # row 1, column 0
  ax.scatter(summ[:,1], X[:,0], marker="+", s=30, label="truth")
  ax.scatter(summ[:,1], estm_clr_time[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("abs_clr_error(s)")
  ax.set_xlabel("exp_time(s)")

  ax = plt.subplot(gs[0, 1]) # row 0, column 1
  ax.scatter(np.sqrt(summ[:,0]), Y[:,0], marker="+", s=30, label="truth")
  ax.scatter(np.sqrt(summ[:,0]), estm_error[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("abs_clr_error(s)")
  ax.set_xlabel("distance^0.5(m^0.5)")

  ax = plt.subplot(gs[1, 1]) # row 1, column 1
  ax.scatter(summ[:,1], Y[:,0], marker="+", s=30, label="truth")
  ax.scatter(summ[:,1], estm_error[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("abs_clr_error(s)")
  ax.set_xlabel("exp_time(s)")

  plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)

  plt.show()

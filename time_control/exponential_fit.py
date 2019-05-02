#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import argparse
import csv
import math

from scipy.optimize import curve_fit


def Scale(x):
    maximum = np.max(x)
    minimum = np.min(x)
    return (x-minimum)/(maximum-minimum)

def Descale(y, maximum, minimum):
    return y*(maximum-minimum)+minimum

def Exp_Func(X, a, b, c):
    return a+b*np.exp(X/c)

def Exp_Fit(X):
    init_X = X.copy()
    maximum = []
    minimum = []
    it = 1
    while True:
        maximum.append(np.max(X[:,0]))
        minimum.append(np.min(X[:,0]))
        X[:,0] = Scale(X[:,0])
        para = curve_fit(Exp_Func, X[:,1], X[:,0])[0]
        estm = Exp_Func(X[:,1], para[0], para[1], para[2])
        estm = np.array(estm)
        dlt = []
        for i in range(0, len(estm)):
            if abs(estm[i] - X[i,0]) >= 0.2:
                dlt.append(i)
        if dlt == []:
            break
        else:
            X = np.delete(X, dlt, 0)
            np.array(X)
            it += 1

    print("a = ", para[0])
    print("b = ", para[1])
    print("c = ", para[2])
    estimate = Exp_Func(init_X[:,1], para[0], para[1], para[2])
    for i in range(0, it):
        estimate = Descale(estimate, maximum[it-i-1], minimum[it-i-1])

    return estimate
    

    
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

  X = np.zeros((len(summ), 2))
  X[:,0] = summ[:,3]/summ[:,1]
  X[:,1] = Scale(summ[:,1])

  Y = np.zeros((len(summ), 2))
  Y[:,0] = summ[:,3]/summ[:,1]
  Y[:,1] = Scale(summ[:,3])
      
  estimate1 = Exp_Fit(X)
  estimate2 = Exp_Fit(Y)
  

  # Create 2x1 sub plots
  gs = gridspec.GridSpec(2, 1)
  fig = plt.figure()

  ax = plt.subplot(gs[0, 0]) # row 0
  ax.scatter(summ[:,1], summ[:,3]/summ[:,1], marker="+", s=30, label="truth")
  ax.scatter(summ[:,1], estimate1[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("rlt_clr_exp")
  ax.set_xlabel("exp_time(s)")

  ax = plt.subplot(gs[1, 0]) # row 1
  ax.scatter(summ[:,1], summ[:,3]/summ[:,1], marker="+", s=30, label="truth")
  ax.scatter(summ[:,1], estimate2[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("rlt_clr_exp")
  ax.set_xlabel("color_time(s)")

  plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)

  plt.show()

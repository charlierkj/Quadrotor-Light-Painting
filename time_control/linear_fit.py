#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import argparse
import csv
import math

from scipy.optimize import curve_fit


def Lnr_Func(X, a, b):
    return a+b*X    

    
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

  X = []
  for s in summ:
      x = []
      x.append(s[1])
      x.append(s[3])
      X.append(x)

  X = np.array(X)
  
  para1 = curve_fit(Lnr_Func, X[:,1], X[:,0])[0]
  
  print("to estimate exp_time using color_time")
  print("a = ", para1[0])
  print("b = ", para1[1])
  print("\n")
  
  estm1 = Lnr_Func(X[:,1], para1[0], para1[1])
  estm1 = np.array(estm1)

  Y = []
  for s in summ:
      y = []
      y.append(s[2])
      y.append(s[1])
      Y.append(y)

  Y = np.array(Y)
  
  para2 = curve_fit(Lnr_Func, Y[:,1], Y[:,0])[0]

  print("to estimate true_time using exp_time")
  print("a = ", para2[0])
  print("b = ", para2[1])
  
  estm2 = Lnr_Func(Y[:,1], para2[0], para2[1])
  estm2 = np.array(estm2)


  # Create 2x1 sub plots
  gs = gridspec.GridSpec(2, 1)
  fig = plt.figure()

  ax = plt.subplot(gs[0, 0]) # row 0
  ax.scatter(summ[:,3], summ[:,1], marker="+", s=30, label="truth")
  ax.scatter(summ[:,3], estm1[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("exp_time(s)")
  ax.set_xlabel("color_time(s)")

  ax = plt.subplot(gs[1, 0]) # row 1
  ax.scatter(summ[:,1], summ[:,2], marker="+", s=30, label="truth")
  ax.scatter(summ[:,1], estm2[:], marker="x", s=30, label="estimate")
  ax.set_ylabel("true_time(s)")
  ax.set_xlabel("exp_time(s)")

  plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)

  plt.show()

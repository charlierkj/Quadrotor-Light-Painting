#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import argparse
import csv


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="plot summary")
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

  error = []
  for sm in summ:
      err = []
      abs_true_error = sm[2] - sm[1]
      rlt_true_error = abs_true_error/sm[1]
      abs_clr_error = sm[3] - sm[2]
      rlt_clr_error = abs_clr_error/sm[2]
      rlt_clr_true = sm[3]/sm[2]
      rlt_clr_exp = sm[3]/sm[1]
      err.append(abs_true_error)
      err.append(rlt_true_error)
      err.append(abs_clr_error)
      err.append(rlt_clr_error)
      err.append(rlt_clr_true)
      err.append(rlt_clr_exp)
      error.append(err)
  error = np.array(error)
      
  # Create 3x1 sub plots
  gs = gridspec.GridSpec(3, 1)
  fig = plt.figure()

  ax = plt.subplot(gs[0, 0]) # row 0
  ax.scatter(np.sqrt(summ[:,0]), error[:,2], marker="o", s=30)
  ax.set_ylabel("abs_clr_error(s)")
  ax.set_xlabel("distance^0.5(m^0.5)")

  #ax = plt.subplot(gs[0, 0]) # row 0
  #ax.scatter(summ[:,0], error[:,3], marker="o", s=30)
  #ax.set_ylabel("rlt_clr_error")
  #ax.set_xlabel("distance(m)")

  #ax = plt.subplot(gs[0, 0]) # row 0
  #ax.scatter(summ[:,0], error[:,4], marker="o", s=30)
  #ax.set_ylabel("rlt_clr_true")
  #ax.set_xlabel("distance(m)")

  ax = plt.subplot(gs[1, 0]) # row 1
  ax.scatter(summ[:,1], error[:,2], marker="o", s=30)
  ax.set_ylabel("abs_clr_error(s)")
  ax.set_xlabel("exp_time(s)")

  #ax = plt.subplot(gs[1, 0]) # row 1
  #ax.scatter(summ[:,1], error[:,3], marker="o", s=30)
  #ax.set_ylabel("rlt_clr_error")
  #ax.set_xlabel("exp_time(s)")

  #ax = plt.subplot(gs[1, 0]) # row 1
  #ax.scatter(summ[:,1], error[:,4], marker="o", s=30)
  #ax.set_ylabel("rlt_clr_true")
  #ax.set_xlabel("exp_time(s)")

  ax = plt.subplot(gs[2, 0]) # row 2
  ax.scatter(summ[:,1], error[:,5], marker="o", s=30)
  ax.set_ylabel("rlt_clr_exp")
  ax.set_xlabel("exp_time(s)")

  plt.show()

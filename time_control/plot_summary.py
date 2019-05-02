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
  # Create 3x1 sub plots
  gs = gridspec.GridSpec(3, 1)
  fig = plt.figure()

  ax = plt.subplot(gs[0, 0]) # row 0
  ax.scatter(np.sqrt(summ[:,0]), summ[:,1])
  ax.set_ylabel("expected time(s)")
  ax.set_xlabel("distance^0.5(m^0.5)")

  ax = plt.subplot(gs[1, 0]) # row 1
  ax.scatter(np.sqrt(summ[:,0]), summ[:,2], marker="+", s=30, label="true time")
  ax.scatter(np.sqrt(summ[:,0]), summ[:,3], marker="x", s=30, label="color time")
  ax.set_ylabel("time(s)")
  ax.set_xlabel("distance^0.5(m^0.5)")

  ax = plt.subplot(gs[2, 0]) # row 2
  ax.scatter(summ[:,1], summ[:,2], marker="+", s=30, label="true time")
  ax.scatter(summ[:,1], summ[:,3], marker="x", s=30, label="color time")
  ax.set_ylabel("time(s)")
  ax.set_xlabel("expected time(s)")

  plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)

  plt.show()

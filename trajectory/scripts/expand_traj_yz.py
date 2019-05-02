import numpy as np
import sys
import csv
import math
from numpy.linalg import inv
import argparse

parser = argparse.ArgumentParser(description="expand traj on y-z plane")
parser.add_argument("inputfile", help="input file destination")
parser.add_argument("outputfile", help="output file destination")
args = parser.parse_args()

trajfile = args.inputfile
outputfile = args.outputfile

fy = 1.5
fz = 1.5
trajstr = []

with open(trajfile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        trajstr.append(row)

trajstr = trajstr[1:]
traj = []
for l in trajstr:
    tr = []
    for p in l[:33]:
        tr.append(float(p))
    traj.append(tr)


for p in traj:
    for i in range(0,8):
        p[9+i] *= fy
        p[17+i] *= fz


out = open(outputfile, "w")

out.write("duration,x^0,x^1,x^2,x^3,x^4,x^5,x^6,x^7,y^0,y^1,y^2,y^3,y^4,y^5,y^6,y^7,z^0,z^1,z^2,z^3,z^4,z^5,z^6,z^7,yaw^0,yaw^1,yaw^2,yaw^3,yaw^4,yaw^5,yaw^6,yaw^7\n")

for trj in traj:
    duration = trj[0]
    
    x = np.array(trj[1:9]).tolist()
    y = np.array(trj[9:17]).tolist()
    z = np.array(trj[17:25]).tolist()
    yaw = np.array(trj[25:]).tolist()
    pstr = ""
    pstr += str(duration) + ","
    for i in range(8):
        pstr += str(x[i]) + ","
    for i in range(8):
        pstr += str(y[i]) + ","
    for i in range(8):
        pstr += str(z[i]) + ","
    for i in range(7):
        pstr += str(yaw[i]) + ","
    pstr += str(yaw[-1])
    out.write(pstr + "\n")
out.close()

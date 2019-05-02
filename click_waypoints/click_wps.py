import numpy as np
import argparse

from PIL import Image
from pylab import *

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="click waypoints")
  parser.add_argument("outputfile", help="output file destination")
  args = parser.parse_args()

  outputfile = args.outputfile

  image = np.array(Image.open('magic.jpg'))
  width = shape(image)[1]
  height = shape(image)[0]
  imshow(image)

  print("width (pixel):",width)
  print("height (pixel):", height)
  print("Please click 29 points")

  wps = np.array(ginput(29, -1))
  #print(wps)

  for waypoint in wps:
      waypoint[1] = height - waypoint[1]
  #print(wps)

  origin = wps[0].copy()
  #print(origin)
 
  for waypoint in wps:
      waypoint -= origin
  #print(wps)


  out = open(outputfile, "w")

  for waypoint in wps:
      x = 0
      y = waypoint[0]/width*4
      z = waypoint[1]/height*2
      pstr = ""
      pstr += str(x) + "," + str(y) + "," + str(z) + "\n"
      out.write(pstr)
  out.close()

  

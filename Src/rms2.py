""" Rms : Compute rms of binary data """

import sys
import argparse
import numpy as np
import babin as ba
from math import *

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Define options

#---------------------------------------------------------------------
#Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
#---------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Program to compute rms")
parser.add_argument("fin",help="Input binary file")
parser.add_argument("-v",dest="v",action='store_true',help="Verbose flag")



parser.add_argument("-n1",dest="n1",type=int,default=1,
                        help="First dimension of data")
parser.add_argument("-n2",dest="n2",type=int,default=1,
                        help="second dimension of data")
parser.add_argument("-n3",dest="n3",type=int,default=1,
                        help="second dimension of data")
#Parse arguments
args = parser.parse_args()
n1=args.n1
n2=args.n2
n3=args.n3
      


#Get the data
fin = ba.bin(args.fin)
data=fin.read((n3,n2,n1))

#Compute rms value, max and min.
pmax=0.0
pmin=0.0
for k in range(0,n3):
  for j in range(0,n2):
    for i in range(0,n1):
      if data[k,j,i] > pmax :
        pmax= data[k,j,i]
        posmax=[k,j,i]
      if data[k,j,i] < pmin :
        pmin= data[k,j,i]
        posmin=[k,j,i]

rms = sqrt(np.mean(np.square(data)))
max = np.amax(data)
min = np.amin(data)

if args.v :
    print("** max value: ", max)
    print("** min value: ", min)
    print("** rms value: ", rms)
    print("** pmax value: ", pmax)
    print("** pmax value at pos: ", pmax, posmax)
    print("** pmin value at pos: ", pmin, posmin)
else :
    print(rms)

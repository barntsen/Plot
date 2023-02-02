""" Scale : Scale binary data """

from __future__ import print_function
import sys
import argparse
import numpy as np
import babin as ba

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Define options

#---------------------------------------------------------------------
#Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
#---------------------------------------------------------------------
parser = argparse.ArgumentParser(description="program to normalizei data")
parser.add_argument("fin",help="Input binary file")
parser.add_argument("fout",help="Output binary file")
parser.add_argument("-s",dest="s",type=float,default=1.0,help="scale factor")
parser.add_argument("-n",dest="n",action='store_true',help="normalize with max value")

#Parse arguments
args = parser.parse_args()


#Get the data
fin = ba.bin(args.fin)
data=fin.readb()

if(args.n == 1) :
    max = abs(np.amax(data))
    print("max: ", max)
    min = abs(np.amin(data))
    if(abs(min) >= max) :
        max = min
    if(max == 0.0) :
        max=1.0  
else :
    max=1.0


#scale the data and normalize
data = (args.s/max)*data

fout = ba.bin(args.fout,"w")
fout.write(data)

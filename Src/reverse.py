""" Reverse : Reverse the order along axis of 3D cube"""

from __future__ import print_function
import matplotlib
matplotlib.use('TKAgg')
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import babin as ba
import matplotlib.animation as animation

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Define options

#---------------------------------------------------------------------
#Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
#---------------------------------------------------------------------
parser = argparse.ArgumentParser(description="program to reverse one axis of a binary cube")
parser.add_argument("fin",help="Input binary file")
parser.add_argument("fout",help="Output binary file")
parser.add_argument("-n1",dest="n1",type=int,help="first dimension of data")
parser.add_argument("-n2",dest="n2",type=int,default=1,help="second dimension of data")
parser.add_argument("-n3",dest="n3",type=int,default=1,help="third dimension of data")
parser.add_argument("-ax",dest="ax",type=int,default=1,help="axis to reverse (1,2,3)")

#Parse arguments
args = parser.parse_args()

# Axis
if args.n1 is not None:
    n1 = args.n1
else :
    sys.exit("Missing n1!")

if args.ax is not None:
    ax = args.ax
else :
    ax = 1

n2 = args.n2
n3 = args.n3

#Get the data
fin = ba.bin(args.fin)
data=fin.read((n3,n2,n1))

#Reverse the data
if(ax == 1) :
    rev = data[:,:,::-1] 
elif(ax == 2) :
    rev = data[:,::-1,:] 
elif(ax == 3) :
    rev = data[::-1,:,:] 
else :
    sys.exit("Uknown axis")

#write the data

fout = ba.bin(args.fout,"w")
fout.write(rev)





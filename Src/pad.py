""" Pad : pad 3D data cube """

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
parser = argparse.ArgumentParser(description="program to window a binary cube")
parser.add_argument("fin",help="Input binary file")
parser.add_argument("fout",help="Output binary file")
parser.add_argument("-n1",dest="n1",type=int,help="first dimension of data")
parser.add_argument("-n2",dest="n2",type=int,default=1,help="second dimension of data")
parser.add_argument("-n3",dest="n3",type=int,default=1,help="third dimension of data")
parser.add_argument("-nb",dest="nb",type=int,default=0,help="Length of padding at the start of axis")
parser.add_argument("-ne",dest="ne",type=int,default=0,help="Length of padding at the end of axis")
parser.add_argument("-ax",dest="ax",type=int,default=1,help="axis to pad")

#Parse arguments
args = parser.parse_args()

# Axis
if args.n1 is not None:
    n1 = args.n1
else :
    sys.exit("Missing n1!")

n2 = args.n2
n3 = args.n3
nb = args.nb
ne = args.ne
ax = args.ax

if n1 <= 0 :
    sys.exit("n1 0 or negative \n")
if n2 <= 0 :
    sys.exit("n2 0 or negative \n")
if n3 <= 0 :
    sys.exit("n3 0 or negative \n")

if(nb < 0):
    sys.exit("nb  negative \n")
if(ne < 0):
    sys.exit("ne  negative \n")

#Get the data
fin = ba.bin(args.fin)
data=fin.read((n3,n2,n1))

if (ax == 1) :
    pad = np.zeros((n3,n2,n1+nb+ne))
    pad[:,:,nb:n1+nb]=data[:,:,:]
    #pad start of x-axis with boundary value
    for k in range(0,n3) :
        for j in range(0,n2) :
            for i in range(0,nb) :
                pad[k,j,i] = data[k,j,0]

    #pad end of x-axis with boundary values
    for k in range(0,n3) :
        for j in range(0,n2) :
            for i in range(0,ne) :
                pad[k,j,i+n1] = data[k,j,n1-1]
elif (ax == 2) :
    pad = np.zeros((n3,n2+nb+ne,n1))
    pad[:,nb:n1+nb,:]=data[:,:,:]
    #pad start of y-axis with boundary value
    for k in range(0,n3) :
        for j in range(0,nb) :
            for i in range(0,n1) :
                pad[k,j,i] = data[k,0,i]

    #pad end of y-axis with boundary values
    for k in range(0,n3) :
        for j in range(0,ne) :
            for i in range(0,n1) :
                pad[k,j+n2,i] = data[k,n2-1,i]

elif (ax == 3) :
    pad = np.zeros((n3+nb+ne,n2,n1))
    #pad start of z-axis with boundary value
    for k in range(0,n3) :
        for j in range(0,nb) :
            for i in range(0,n1) :
                pad[k,j,i] = data[0,j,i]

    #pad end of x-axis with boundary values
    for k in range(0,n3) :
        for j in range(0,ne) :
            for i in range(0,n1) :
                pad[k+n3,j,i] = data[k,n2-1,i]

else :
    sys.exit("Illegal axis \n")

#write the data
fout = ba.bin(args.fout,"w")
fout.write(pad)

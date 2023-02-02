""" Fdecon : Frequency domain interpolation """

from __future__ import print_function
from math import *
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
parser.add_argument("-n1",dest="n1",type=int,help="First Dimension of data")
parser.add_argument("-n2",dest="n2",type=int,help="Second Dimension of data")
parser.add_argument("-opr",dest="opr",help="Input operator file")

#Parse arguments
args = parser.parse_args()

# Axis
if args.n1 is not None:
    n1 = args.n1
else :
    sys.exit("Missing n1!")

if args.n2 is not None:
    n2 = args.n2
else :
    n2 = 1

if args.opr is not None:
    opr = args.opr
else :
    sys.exit("Missing operator file")

#Get the data
fin = ba.bin(args.fin)
din=fin.read((n2,n1))
fout = ba.bin(args.fout,'w')
fopr = ba.bin(opr)
dopr = fopr.read((n2,n1))
dout = np.zeros((n2,n1))
print("dout: ", dout.shape)

#Compute Fourier transform of input data
fdin = np.fft.fft(din,2*n1,1)
fdopr = np.fft.fft(dopr,2*n1,1)

#Compute convolution
fdout = fdin*fdopr
tmp=np.real(np.fft.ifft(fdout,2*n1,1))
dout[:,0:n1] = tmp[:,0:n1]
fout.write(dout)



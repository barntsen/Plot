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
parser.add_argument("-n3",dest="n2",type=int,help="Third Dimension of data")
parser.add_argument("-d1",dest="d1",type=float,help="sampling interval")
parser.add_argument("-opr",dest="opr",help="Input operator file")
parser.add_argument("-t0",dest="t0",type=float,help="Time delay")

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

if args.d1 is not None:
    d1 = args.d1
else:
    d1=1.0

if args.t0 is not None:
    t0 = args.t0
else:
    t0=0.0

#Get the data
fin = ba.bin(args.fin)
din=fin.read((n2,n1))
fout = ba.bin(args.fout,'w')
fopr = ba.bin(opr)
dopr = fopr.read((n2,n1))
dout = np.zeros(n1)
print("dout: ", dout.shape)

#Compute Fourier transform of input data
fdin = np.fft.fft(din,2*n1,1)
fdopr = np.fft.fft(dopr,2*n1,1)

#Compute least squares estimate
amp = np.abs(fdopr)
eps = 0.1*np.amax(amp)
df = 1.0/(n1*d1)
fdout = (fdin*np.conj(fdopr))/(fdopr*np.conj(fdopr) + eps)

for l in range(0,n2):
  for i in range(0,int(n1)) :
    fdout[l,i] = fdout[l,i]*np.exp(-1j*i*(2.0*pi*df*t0))
  for i in range(int(n1),0,-1):
    fdout[l,2*n1-i] = fdout[l,i]*np.exp(1j*i*(2.0*pi*df*t0))

tmp=np.real(np.fft.ifft(fdout,2*n1,1))
for i in range(0,n2):
  dout[0:n1] = tmp[i,0:n1]+dout[0:n1]
fout.write(dout)



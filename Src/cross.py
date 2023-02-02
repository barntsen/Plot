""" Rms : Compute rms of binary data """
from __future__ import print_function
import sys
import argparse
import numpy as np
import babin as ba
from math import *

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def xcross(a,b) :
        n=a.shape[0]
        A = np.fft.fft(a,2*n)
        B = np.fft.fft(b,2*n)
        C = B*np.conj(A)
        c = np.fft.fftshift(np.fft.ifft(C))
        #c = np.fft.ifft(C)
        #val = np.real(c[0:n])
        val = np.real(c)
        return(val)

# Define options

#---------------------------------------------------------------------
#Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
#---------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Program to compute rms")
parser.add_argument("f1",help="Input binary file")
parser.add_argument("f2",help="Input binary file")
#parser.add_argument("fout",help="Output binary file")
#parser.add_argument("-s",dest="s",type=float,default=1.0,help="scale factor")
#parser.add_argument("-n",dest="n",action='store_true',help="normalize with max value")

#Parse arguments
args = parser.parse_args()


#Get the data
fin = ba.bin(args.f1)
data1=fin.readb()

#Get the data
fin = ba.bin(args.f2)
data2=fin.readb()

#Compute cross correlation 
out = xcross(data1,data2)



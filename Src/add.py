""" Add : add or subtract two binary files """
from __future__ import print_function
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
    if (arg[0] == '-') and (len(arg) > 1 ) : 
        if arg[1].isdigit(): 
            sys.argv[i] = ' ' + arg
#---------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Program to compute rms")
parser.add_argument("f1",help="Input binary file")
parser.add_argument("f2",help="Input binary file")
parser.add_argument("fout",help="Output binary file")
parser.add_argument("-op",dest="op",default="+",help="Operation + -")

#Parse arguments
args = parser.parse_args()


#Get the data
fin = ba.bin(args.f1)
data1=fin.readb()

#Get the data
fin = ba.bin(args.f2)
data2=fin.readb()

if args.op == '-' :
    print(" op: - ")
    #Compute difference
    diff = data1-data2
elif args.op == '+' :
    print(" op: + ")
    #Compute sum
    diff = data1+data2
elif args.op == '*' :
    print(" op: * ")
    #Compute sum
    diff = data1*data2
elif args.op == '/' :
    print(" op: / ")
    #Compute sum
    diff = data1/data2
else :
    print("Illegal operation")
    

fout= ba.bin(args.fout,"w")
fout.write(diff)

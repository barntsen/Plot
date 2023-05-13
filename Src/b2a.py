""" Window : window data in a 3D binary cube """

import sys
import argparse
import numpy as np
import babin as ba

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Define options
#Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
parser = argparse.ArgumentParser(description="program to window a binary cube")
parser.add_argument("fin",help="Input binary file")
#parser.add_argument("fout",help="Output binary file")
parser.add_argument("-n1",dest="n1",type=int,help="first dimension of data")
parser.add_argument("-n2",dest="n2",type=int,default=1,help="second dimension of data")
parser.add_argument("-n3",dest="n3",type=int,default=1,help="third dimension of data")
parser.add_argument("-f1",dest="f1",type=int,default=0,help="start of window in first dimension")
parser.add_argument("-f2",dest="f2",type=int,default=0,help="start of window in second dimension")
parser.add_argument("-f3",dest="f3",type=int,default=0,help="start of window in third dimension")
parser.add_argument("-l1",dest="l1",type=int,default=0,help="length of window in first dimension")
parser.add_argument("-l2",dest="l2",type=int,default=0,help="length of window in second dimension")
parser.add_argument("-l3",dest="l3",type=int,default=0,help="length of window in third dimension")
parser.add_argument("-i1",dest="i1",type=int,default=1,help="increment in first dimension")
parser.add_argument("-i2",dest="i2",type=int,default=1,help="increment in second dimension")
parser.add_argument("-i3",dest="i3",type=int,default=1,help="increment in second dimension")
parser.add_argument("-min1",dest="min1",type=float,
                            help="start of window in first dimension (in units)")
parser.add_argument("-min2",dest="min2",type=float,
                            help="start of window in second dimension (in units)")
parser.add_argument("-min3",dest="min3",type=float,
                            help="start of window in third dimension (in units)")
parser.add_argument("-len1",dest="len1",type=float,
                            help="length of window in first dimension (in units)")
parser.add_argument("-len2",dest="len2",type=float,
                            help="length of window in second dimension (in units)")
parser.add_argument("-len3",dest="len3",type=float,
                            help="length of window in second dimension (in units)")
parser.add_argument("-inc1",dest="inc1",type=float,
                            help="Increment in first dimension (in units)")
parser.add_argument("-inc2",dest="inc2",type=float,
                            help="Increment in second dimension (in units)")
parser.add_argument("-inc3",dest="inc3",type=float,
                            help="Increment in second dimension (in units)")
parser.add_argument("-d1",dest="d1",type=float,default=1.0,
                          help="sampling interval in first dimension")
parser.add_argument("-d2",dest="d2",type=float,default=1.0,
                          help="sampling interval in second dimension")
parser.add_argument("-d3",dest="d3",type=float,default=1.0,
                          help="sampling interval in third dimension")
parser.add_argument("-o1",dest="o1",type=float,default=0.0,
                          help="origin in first dimension")
parser.add_argument("-o2",dest="o2",type=float,default=0.0,
                          help="origin in second dimension")
parser.add_argument("-o3",dest="o3",type=float,default=0.0,
                          help="origin in third dimension")
parser.add_argument("-x",dest="x",type=float,default=0,
                          help="x-coordinate")
parser.add_argument("-y",dest="y",type=float,default=0,
                          help="y-coordinate")
parser.add_argument("-z",dest="z",type=float,default=0,
                          help="z-coordinate")

#Parse arguments
args = parser.parse_args()

if args.min1 is not None:
    f1 = int((args.min1-args.o1)/args.d1)
else : 
    f1 = args.f1

if args.min2 is not None:
    f2 = int((args.min2-args.o2)/args.d2)
else : 
    f2 = args.f2

if args.min3 is not None:
    f3 = int((args.min3-args.o3)/args.d3)
else : 
    f3 = args.f3

if args.len1 is not None:
    l1 = int(args.len1/args.d1)
else :
    l1 = args.l1

if args.len2 is not None:
    l2 = int(args.len2/args.d2)
else :
    l2 = args.l2

if args.len3 is not None:
    l3 = int(args.len3/args.d3)
else :
    l3 = args.l3

if args.inc1 is not None:
    i1 = int(args.inc1/args.d1)
else :
    i1 = args.i1

if args.inc2 is not None:
    i2 = int(args.inc2/args.d2)
else:
    i2 = args.i2

if args.inc3 is not None:
    i3 = int(args.inc3/args.d3)
else :
    i3 = args.i3

#Axis
if args.n1 is not None:
    n1 = args.n1
else :
    sys.exit("Missing n1!")
n2 = args.n2
n3 = args.n3

#Change default from 0 to full length
if(l1 == 0):
   l1 = n1
if(l2 == 0):
   l2 = n2
if(l3 == 0):
   l3 = n3 

if n1 <= 0 :
    sys.exit("n1 0 or negative \n")
if n2 <= 0 :
    sys.exit("n2 0 or negative \n")
if n3 <= 0 :
    sys.exit("n3 0 or negative \n")

if(f1 < 0):
    sys.exit("f1  negative \n")
if(f2 < 0):
    sys.exit("f2  negative \n")
if(f3 < 0):
    sys.exit("f3  negative \n")

if(l1 <= 0):
    sys.exit("l1 0 or negative\n")
if(l2 <= 0):
    sys.exit("l2 0 or negative\n")
if(l3 <= 0):
    sys.exit("l3 0 or negative\n")

if(f1+l1 > n1):
    print("f1+l1:", f1+l1)
    sys.exit("f1+l1 too large\n")
if(f2+l2 > n2):
    sys.exit("f2+l2 too large\n")
if(f3+l3 > n3):
    sys.exit("f3+l3 too large\n")

#Get the data
fin = ba.bin(args.fin)
data=fin.read((n3,n2,n1))


#print the data
x=args.x
y=args.y
z=args.z
d1=args.d1
o1=args.o1
d2=args.d2
o2=args.o2
d3=args.d3
o3=args.o3
ix = int((x-o1)/d1)
if(ix < 0):
  ix=0
iy = int((y-o2)/d2)
if(iy < 0):
  iy=0
iz = int((z-o3)/d3)
if(iz < 0):
  iz=0

print("x,y,z,value: ", x,y,z,data[iz,iy,ix])

#eprint("** window: output n1 n2 n3: ",win.shape[0], win.shape[1], win.shape[2])


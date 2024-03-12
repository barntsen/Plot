'''Graph: Draw graph '''

import sys
import argparse
import numpy as np
import matplotlib.pyplot as pl
import babin as ba

#---------------------------------------------------------------------
#Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
#---------------------------------------------------------------------

# Define options
parser = argparse.ArgumentParser(description="Graph plot for rsf data file")
parser.add_argument("-o",dest="out",help="Output graphics file")
parser.add_argument("-noshow",dest="noshow",action='store_true',
                      help="turn off plotting to screen if this option is present")
parser.add_argument("-title",dest="title",help="title")
parser.add_argument("-xlabel",dest="xlabel",help="x-axis label")
parser.add_argument("-ylabel",dest="ylabel",help="y-axis label")
parser.add_argument("-xmin",dest="xmin",type=float,help="Minimum x value")
parser.add_argument("-xmax",dest="xmax",type=float,help="Maximum x value")
parser.add_argument("-ymin",dest="ymin",type=float,help="Minimum y value")
parser.add_argument("-ymax",dest="ymax",type=float,help="Maximum y value")
parser.add_argument("-xlog",dest="xlog",action='store_true',help="log x-axis if present")
parser.add_argument("-ylog",dest="ylog",action='store_true',help="log y-axis if present")
parser.add_argument("-ar",dest="ar",type=float,help="Aspect ratio")
parser.add_argument("-normalize",dest="normalize",type=int,help="-normalize 1  to normalize data")
parser.add_argument("-legend",dest="legend",action="append",help="legend text (option can be repeated)")
parser.add_argument("fname",help="Input rsf file")
parser.add_argument("-n1",dest="n1",type=int,help="No of data points")
parser.add_argument("-n2",dest="n2",type=int,help="No of graphs")
parser.add_argument("-d1",dest="d1",type=float,help="Sampling interval along x-axis")
parser.add_argument("-o1",dest="o1",type=float,help="Sampling interval along x-axis")
parser.add_argument("-t",dest="t",action='store_true',
                      help="Transpose x and y axis is this option is present")

#Parse arguments
args = parser.parse_args()

# Axis
if args.n1 is not None:
    n1 = args.n1
else:
    print ("Missing n1!")

if args.n2 is not None:
    n2 = args.n2
else:
    n2 = 1

if args.d1 is not None:
    d1= args.d1
else:
    d1=1.0

if args.o1 is not None:
    o1= args.o1
else:
    o1=0.0

#Load the data
fin = ba.bin(args.fname)
data=fin.read((n2,n1))


# Normalizing data
if  args.normalize is not None:
    datamax = abs(data).max();
    data = data/datamax

if args.t is False :
  ymin = np.amin(data)
  ymax = np.amax(data)
  xmin = o1
  xmax = o1+d1*n1
else :
  xmin = np.amin(data)
  xmax = np.amax(data)
  ymin = o1+d1*n1
  ymax = o1

ar   = 1.0

if args.xmin is not None:
    xmin = args.xmin
if args.xmax is not None:
    xmax = args.xmax
if args.ymin is not None:
    ymin = args.ymin
if args.ymax is not None:
    ymax = args.ymax
if args.ar is not None:
    ar = args.ar

if args.t is True :
  x = np.zeros((n1))
  x = np.linspace(ymin,ymax,n1)
else :
  x = np.zeros((n1))
  x = np.linspace(xmin,xmax,n1)

# Plotting
pl.figure()
pl.ylim(ymin,ymax)
pl.xlim(xmin,xmax)

if args.xlog == True :
  pl.xscale("log")

if args.ylog == True :
  pl.yscale("log")

if args.legend is not None:
    l=0
    for s in args.legend:
        if args.t is True :
          pl.plot(np.flip(data[l,:]),x, label=args.legend[l])
        else :
          pl.plot(x,data[l,:], label=args.legend[l])
        l=l+1
        pl.legend(loc="upper right")
else:
    for l in range(0,n2):
        if args.t is True  :
          pl.plot(np.flip(data[l,:]),x)
        else :
          pl.plot(x,data[l,:])

# Set apsect ratio
ax=pl.gca()
if(ar > 0) :
  asr = 1.0/(ax.get_data_ratio()*ar)
  pl.Axes.set_aspect(ax,asr)

# Set title and labels
if args.title is not None:
    pl.title(args.title)
if args.xlabel is not None:
    pl.xlabel(args.xlabel)
if args.ylabel is not None:
    pl.ylabel(args.ylabel)
if args.out is not None:
    pl.savefig(args.out,bbox_inches='tight')
if args.noshow is False:
    pl.show()



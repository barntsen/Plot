''' Graphxy: Draw graph from ascii xy file'''

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
parser.add_argument("-show",dest="show",help="-show 1 to NOT show graph on screen")
parser.add_argument("-title",dest="title",help="title")
parser.add_argument("-xlabel",dest="xlabel",help="x-axis label")
parser.add_argument("-ylabel",dest="ylabel",help="y-axis label")
parser.add_argument("-xmin",dest="xmin",type=float,help="Minimum x value")
parser.add_argument("-xmax",dest="xmax",type=float,help="Maximum x value")
parser.add_argument("-ymin",dest="ymin",type=float,help="Minimum y value")
parser.add_argument("-ymax",dest="ymax",type=float,help="Maximum y value")
parser.add_argument("-ar",dest="ar",type=float,help="Aspect ratio")
parser.add_argument("-normalize",dest="normalize",type=int,help="-normalize 1  to normalize data")
parser.add_argument("-legend",dest="legend",action="append",help="legend text (option can be repeated)")
parser.add_argument("fname",help="Input rsf file")
#parser.add_argument("-n1",dest="n1",type=int,help="No of data points")
#parser.add_argument("-ng",dest="ng",type=int,help="No of graphs")
#parser.add_argument("-d1",dest="d1",type=float,help="Sampling interval along x-axis")
#parser.add_argument("-o1",dest="o1",type=float,help="Sampling interval along x-axis")

#Parse arguments
args = parser.parse_args()

# Axis
#Load the data
data=np.loadtxt(args.fname)
dims = data.shape
ng = dims[1]-1

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

x = data[:,0]

# Plotting
pl.figure()
if(args.ymin is not None) and (args.ymax is not None) :
    pl.ylim(ymin,ymax)
if(args.xmin is not None) and (args.xmax is not None) :
    pl.xlim(xmin,xmax)

if args.legend is not None:
    l=0
    for s in args.legend:
        pl.plot(x,data[:,l+1],label=args.legend[l])
        l=l+1
        pl.legend(loc="upper right")
else:
    for l in range(0,ng):
        pl.plot(x,data[:,l+1])

# Set apsect ratio
ax=pl.gca()
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
1
if args.show is None:
    pl.show()



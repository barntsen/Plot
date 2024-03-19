'''
Image: reads a data file and plots an image on screen and can also 
output the plot on a file. It is mainly designed for seismic data and
velocity models. 
'''

import matplotlib.pyplot as pl
import sys
import argparse
import numpy as np
import parula
import bacolmaps
import babin as ba
from pltcom import *
import rss as rs

## Get command line options

# Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg

# Heading
parser = argparse.ArgumentParser(description="Script for plotting  2D seismic data and velocity models")

parser = comargs(parser)
# Parse arguments
args = parser.parse_args()

# Axis
if args.n1 is not None:
    n1 = args.n1
else :
    n1 = -1

if args.d1 is not None:
    d1 = args.d1
else :
    d1 = 1.0

if args.o1 is not None:
    o1 = args.o1
else :
    o1 = 0.0

if args.n2 is not None:
    n2 = args.n2
else :
    n2 = -1

if args.d2 is not None:
    d2 = args.d2
else :
    d2 = 1.0

if args.o2 is not None:
    o2 = args.o2
else :
    o2 = 0.0

if args.t is True:
    transp = 1;
else:
    transp = 0; 

#First install custom colormaps
bacolmaps.cmap('crust')
parula.setcolors()


#Get the data
data =getdata(args.fname,n1,n2)

#Get the background image 
if args.fb is not None :
    bg=getdata(args.fname)

if(transp == 1):
    data=data.transpose()
    if(args.fb is not None):
        bg=bg.transpose()
    tmp = o2
    o2  = o1
    o1  = tmp
    tmp = d2
    d2  = d1
    d1  = tmp
    tmp = n1
    n1  = n2
    n2  = tmp 

ar=1.0

#--------------------------------------------------------------------
# Get scaling parameters
#---------------------------------------------------------------------
#Print min,max and absmax of data set:
amps = absmax(data)
mindata = amps[0]
maxdata = amps[1]
absdata = amps[2]

print ("=== min,max,absmax values of data:", amps)

#Default scaling of data is perecentile clip at 99%
cmin,cmax = pclip(data,99.0)
print ("default cmin,cmax: ", cmin,cmax)

if  args.pclip is not None:
    print ("Calling pclip: ", args.pclip)
    cmin,cmax = pclip(data,args.pclip)
    print ("pclip cmin,cmax: ", cmin,cmax)
if  args.clip is not None:
    cmax = (args.clip/100.0)*absdata
    cmin = -cmax
    print ("clip cmin,cmax: ", cmin,cmax)
if args.cmin is not None:
    cmin = args.cmin
    print ("cmin cmin: ", cmin)
if args.cmax is not None:
    cmax = args.cmax
    print( "cmax cmax: ", cmin)
if args.ar is not None:
    ar = args.ar
else :
    ar = 1.0

print ("=== Final clip values cmin,cmax: ", cmin,cmax)

#Add bias 
if args.bias is not None:
    data = data+args.bias
#-----------------------------------------------------------------------
# Plotting
#-----------------------------------------------------------------------
fig =pl.figure()


#pl.xlim(o1,o1+d1*(n1-1))
#pl.ylim(o2+d2*(n2-1),o2)

#Plot data array
im=pl.imshow(data,clim=(cmin,cmax),cmap=args.colormap,
          extent=[o1,o1+d1*n1,o2+d2*n2,o2])  

#Plot also background array
if args.fb is not None :
    pl.imshow(bg,alpha=args.trans,cmap=cmap_vp,
              extent=[o1,o1+d1*n1,o2+d2*n2,o2],interpolation='spline36')  


#Set aspect ratio
ax=pl.gca()
asr = 1.0/(ax.get_data_ratio()*ar)
pl.Axes.set_aspect(ax,asr)

if args.colorbar is not None : 
    cbar=pl.colorbar(im,fraction=0.02, pad=0.04)


#Title and axis decorations
if args.title is not None:
    pl.title(args.title)
if args.xlabel is not None:
    pl.xlabel(args.xlabel)
if args.ylabel is not None:
    pl.ylabel(args.ylabel)
if args.cbtitle is not None:
    cbar.ax.set_title(args.cbtitle)

#Output plot
if args.out is not None:
    fname=args.out
    pl.savefig(fname,bbox_inches='tight')

#Show on screen
if args.noshow is False:
    pl.show()

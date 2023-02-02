'''Make video movie

This scripts reads a binary file of frames (snapshots) and outputs
an animated video (mp4) file. It is mainly designed for snapshots
from seismic modeling programs.
'''

import matplotlib
matplotlib.use('TKAgg')
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import babin as ba
import matplotlib.animation as animation
import parula
from pltcom import *
#---------------------------------------------------------------------
#Get coomand line options
#---------------------------------------------------------------------

#Hack for negative floats as option
for i, arg in enumerate(sys.argv):
  if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
#---------------------------------------------------------------------
parser = argparse.ArgumentParser(description='''Animation program for 3D 
           binary data cube''')
parser.add_argument("-noshow",dest="noshow",action='store_true',
           help="turn off plotting to screen if this option is present")
parser.add_argument("-normalize",dest="normalize",action='store_true',
           help="Normalize data if this option is present")
parser.add_argument("-colorbar",dest="colorbar",action='store_true',
           help="Plot colorbar if this option is present")
parser.add_argument("-o",dest="out",
           help="output graphics file")
parser.add_argument("-title",dest="title",
           help="Title of plot, default: None")
parser.add_argument("-xlabel",dest="xlabel",
           help="x-axis label, default: None")
parser.add_argument("-ylabel",dest="ylabel",
           help="y-axis label, default: None")
parser.add_argument("-cmax",dest="cmax",type=float,
           help="Maximum clip value, defualt calculated from data")
parser.add_argument("-cmin",dest="cmin",type=float,
           help="Minimum clip value, defult: -cmax")
parser.add_argument("-ar",dest="ar",type=float,
           help="Aspect ratio, default: 1.0")
parser.add_argument("fname",
           help='''input binary file , format is 
                 float numbers interpreted as a 3D array.''')
parser.add_argument("-fbg",dest="fbg",
           help="input binary velocity file")
parser.add_argument("-bias",dest="bias",default=0.0,type=float,
           help="add a constant to the data, default: 0.0")
parser.add_argument("-colormap",dest="colormap",default="gray",
           help="Color map, default: grey scale")
parser.add_argument("-pclip",dest="pclip",type=float,default=99.0,
           help="percentile clip in percent, defult: 99.0")
parser.add_argument("-clip",dest="pclip",type=float,default=99.0,
           help="clip in percent of max value, default: 99.0")
parser.add_argument("-n1",dest="n1",type=int,
           help="first dimension of data")
parser.add_argument("-n2",dest="n2",type=int,
           help="second dimension of data")
parser.add_argument("-n3",dest="n3",type=int,
           help="third dimension of data, animation direction")
parser.add_argument("-d1",dest="d1",type=float,default=1.0,
           help="first dimension sampling interval, default: 1.0")
parser.add_argument("-d2",dest="d2",type=float,default=1.0,
           help="second dimension sampling interval, default: 1.0")
parser.add_argument("-d3",dest="d3",type=float,default=1.0,
           help="third dimension sampling interval, default: 1.0")
parser.add_argument("-o1",dest="o1",type=float,default=0.0,
           help="first dimension origo, default: 0.0")
parser.add_argument("-o2",dest="o2",type=float,default=0.0,
           help="second dimension origo, default 0.0")
parser.add_argument("-o3",dest="o3",type=float,default=0.0,
           help="third dimension origo, defaullt 0.0")
parser.add_argument("-mfs",dest="mfs",type=int,default=100,
           help="delay between frames, default: 100")
parser.add_argument("-flip",dest="flip",
           help="flip y-axis, default: None")
parser.add_argument("-trans",dest="trans",type=float,default=0.25,
           help="transparency default: 0.25")

#Parse arguments
args = parser.parse_args()

# Axis
if args.n1 is not None:
    n1 = args.n1
else :
    print "Missing n1!"

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
    print "Missing n2!"

if args.d2 is not None:
    d2 = args.d2
else :
    d2 = 1.0

if args.o2 is not None:
    o2 = args.o2
else :
    o2 = 0.0

if args.n3 is not None:
    n3 = args.n3
else :
    print "Missing n3!"

if args.d3 is not None:
    d3 = args.d3
else :
    d3 = 1.0

if args.o3 is not None:
    o3 = args.o3
else :
    o3 = 0.0

if args.flip is not None:
    flip = 1
else :
    flip = 0
    
#Get the data
fin = ba.bin(args.fname)
data=fin.read((n3,n2,n1))

#Get the bacxkground data
if args.fbg is not None :
    fin = ba.bin(args.fbg)
    bg=fin.read((n2,n1))
    background = True
else :
    background = False
#
#Get scaling parameters
#

#Print min,max and absmax of data set:
amps = absmax(data)
mindata = amps[0]
maxdata = amps[1]
absdata = amps[2]

print "=== min,max,absmax values of data:", amps

#Default scaling of data is perecentile clip at 99%
cmin,cmax = pclip(data,99.0)

if  args.pclip is not None:
    cmin,cmax = pclip(data,args.pclip)
if  args.clip is not None:
    cmax = (args.clip/100.0)*absdata
    cmin = -cmax
if args.cmin is not None:
    cmin = args.cmin
if args.cmax is not None:
    cmax = args.cmax
if args.ar is not None:
    ar = args.ar
else :
    ar = 1.0

print "=== Final clip values cmin,cmax: ", cmin,cmax

#Add bias
if args.bias is not None:
    data = data+args.bias

#Normalize the data
if  args.normalize is True:
    data = norm(data)

cnt = 0 #No of frames
inc = 1 #Increment between frames

#-----------------
# Animation
#-----------------
animrun=True   #If true, movie runse
#Figure to animate

fig = plt.figure()
parula.setcolors()
img = data[cnt,:,:]

#Plot frame no 0
im=plt.imshow(img,interpolation='nearest',clim=(cmin,cmax),
              cmap=args.colormap,extent=[o1,o1+d1*n1,o2+d2*n2,o2],animated=True)

#Plot background model
if background == True :
    vl=plt.imshow(bg,interpolation='nearest',alpha=args.trans,
    extent=[o1,o1+d1*n1,o2+d2*n2,o2],cmap="parula",animated=True)

#Set sensible aspcet ratio (The logic behind the aspect ratio this is weird)
ax=plt.gca()
asr = 1.0/(ax.get_data_ratio()*ar)
plt.Axes.set_aspect(ax,asr)

if args.title is not None :
    plt.title(args.title)
if args.xlabel is not None:
    plt.xlabel(args.xlabel)
if args.ylabel is not None:
    plt.ylabel(args.ylabel)

#
# Start the animation loop, frames are updated by calling updatefig
#
ani = animation.FuncAnimation(fig, updatefig, frames=n3-1, repeat=False, interval=args.mfs, blit=True)
plt.show() #Show each frame

#Output the animation in mp4 format.
if args.out is not None:
    ani.save(args.out, writer='ffmpeg', fps=15)


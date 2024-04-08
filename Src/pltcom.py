'''Common plotting functions

This module contains functions for reading and scaling scaling data

Functions:
    absmax: Return absolute maximum value of numpy array
    norm  : Normalize 2d numpy array
    pclip : Get clip values based on perecntiles
'''

import numpy as np
import sys
import os
import babin as ba
import RSSPython as rs
import segy
import argparse


def eprint(*args):
  ''' Print message on standard error and exit

  Arguments:
    *arg: variable comma separated list of strings to be printed

  Returns:
     None

  '''

  print(*args, file=sys.stderr)  
  sys.exit(1)

def getdata(fname, args, n1=0, n2=0) :
    """ Read data in binary, su or rss format"""

    #Get file extension
    fname,format=os.path.splitext(fname)
    fname=fname+format

    if format == '.bin' :
      fin = ba.bin(fname)
      if (n1 == 0) or (n2 == 0) :
        eprint("n1 or n2 or both are zero")
      data=fin.read((n2,n1))
    elif format == '.rss' :
      rsfile = rs.RSSdata()
      rsfile.read(fname)
      print("geomN: ", rsfile.geomN)
      n1 = rsfile.geomN[0][0]
      n2 = rsfile.geomN[2][0]
      args.d1 = rsfile.geomD[0][0]
      args.d2 = rsfile.geomD[2][0]
      o1 = rsfile.geomO[0][0]
      o2 = rsfile.geomO[2][0]
      if(rsfile.type == 2):
        n1 = rsfile.geomN[0][0]
        n2 = rsfile.geomN[1][0]
      if(rsfile.type == 3):
        print("image: 3D data can not be plotted")
      
      data = np.reshape(rsfile.data,[n1,n2])
      data = np.transpose(data)
      
    elif format == '.su' :
      fp = open(fname,"rb")
      trhds,traces = segy.readtrs(fp,-1,"su")
      ntr = len(trhds)
      data = np.transpose(traces)
    else :
      eprint("image : Unknown data format") 
    return data
def absmax(data) :
    ''' Return absolute maximum value of numpy array

    Arguments:
        data: input 2d numpy array

    Returns:
        cmin,cmax,absmax: tuple with minimum value, maximum value and
                          absolute maximum value
    '''

    max = np.amax(data)
    min = np.amin(data)
    amax = abs(max)
    amin = abs(min)

    if amax >= amin :
        absmax = amax
    else :
        absmax = amin

    return((min,max,absmax))

def norm(data) :
    ''' Normalize 2d numpy array

    Arguments:
        data: input 2d numpy array

    Return values:
        ndata: data array divided by absolute maximum
    '''

    maxval = absmax(data)
    if maval > 0.0 :
       ndata = data/maxval
    else :
       ndata = 0.0

    return(ndata)

def pclip(data,pclip) :
    ''' Get clip values based on perecntiles

    Arguments:
        data: input 2d numpy array
        pclip: Clip value in percent of percentiles

    Return values:
        cmin,cmax: tuple with minimum and maximum clip values
    '''

    flat=data.flatten()
    n = flat.shape[0]
    datasort =np.sort(flat,axis=None)
    pindex = int(n*(pclip/100.0))
    cmax=datasort[pindex-1]
    pindex = int(n*((100.0-pclip)/100.0))
    if(pindex < n):
        cmin=datasort[pindex]
    else :
        cmin = datasort[n-1]

    return((cmin,cmax))



def comargs(parser) :
  """Get common command line arguments """

  # Hack for negative floats as option
  for i, arg in enumerate(sys.argv):
    if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg

  parser.add_argument("-o",dest="out",
                         help="Output graphics file")
  parser.add_argument("-title",dest="title",
                         help="Plot title")
  parser.add_argument("-xlabel",dest="xlabel",
                         help="x-axis label")
  parser.add_argument("-ylabel",dest="ylabel",
                         help="y-axis label")
  parser.add_argument("-cmin",dest="cmin",type=float,
                        help="Minimum clip value")
  parser.add_argument("-cmax",dest="cmax",type=float,
                        help="Maximum clip value")
  parser.add_argument("-ar",dest="ar",type=float,
                        help="Aspect ratio")
  parser.add_argument("fname", 
                        help="Input file")
  parser.add_argument("-bias",dest="bias",default=0.0,type=float,
                        help="Add a constant to the data")
  parser.add_argument("-colormap",dest="colormap",default="gray",
                        help="matplotlib standard colormaps + new map: parula")
  parser.add_argument("-bcolormap",dest="bcolormap",default="jet",
                        help="matplotlib standard colormaps + new map: parula")
  parser.add_argument("-pclip",dest="pclip",type=float,
                        help="percentile clip in percentage (default 99)")
  parser.add_argument("-clip",dest="clip",type=float,
                        help="clip in percentage of max value")
  parser.add_argument("-n1",dest="n1",type=int,default=-1,
                        help="First dimension of data")
  parser.add_argument("-n2",dest="n2",type=int,default=-1,
                        help="Second dimension of data")
  parser.add_argument("-d1",dest="d1",type=float,default=1.0,
                        help="First dimension sampling interval")
  parser.add_argument("-d2",dest="d2",type=float,default=1.0,
                        help="Second dimension sampling interval")
  parser.add_argument("-o1",dest="o1",type=float,default=0.0,
                        help="First dimension origo")
  parser.add_argument("-o2",dest="o2",type=float,default=0.0,
                        help="Second dimension origo")
  parser.add_argument("-t",dest="t",action='store_true',
                        help="transpose data if this option is present")
  parser.add_argument("-noshow",dest="noshow",action='store_true',
                   help="turn off plotting to screen if this option is present")
  parser.add_argument("-colorbar",dest="colorbar",action='store_true',
                      help="plot colorbar if this option is present:")
  parser.add_argument("-fb",dest="fb",
                      help="input binary background file. There is no scaling of the background")
  parser.add_argument("-trans",dest="trans",type=float,default=0.25,
                      help="transparency default: 0.25")
  parser.add_argument("-cbtitle",dest="cbtitle",
                         help="Plot title")

  return parser


def circle( origin, r, theta=(0,2*3.14159,0.001) ):
  ''' Create a circle                      
  
    Parameters:
      origin:   tupple with x,y coordinates of circel origin
      r     :   radius of circle
      theta :   Optional argument for the angle range of the circle
                and resolution. theta=(0, 2*pi, dtheta)

  '''
  angle = np.arange(theta[0],theta[1],theta[2])
  print(theta)
  x=np.zeros(len(angle))
  y=np.zeros(len(angle))

  x = r*np.cos(angle)
  y = r*np.sin(angle)

  

  return((x,y))    
  

''' Common functions for error messages, interpolation of 3d grids and map distances

Functions:
    eprint   : Print messages on standard err
    distance : Distance along great circle 
    xyzout   : Dump grid in ascii
    intepol3d: Linear interpolation of 3D grid
    profile  : Extract depth profile from 3D array
    line     : Generate (x,y) coordinates for a straight line

'''


import numpy as np
from math import *
import sys

def eprint(*args):
    ''' Print message on standard error

    Arguments: 
        *arg: variable comma separated list of strings to be printed

    Returns:
        None

    '''

    print(*args, file=sys.stderr)

def distance(minlon,minlat,maxlon,maxlat) :
    ''' Compute distance along great circle 
    
    Arguments: 
        minlon: Start point longitude
        minlat: Start point lattitude
        maxlon: End point lonitude
        maxlat: End point lattitude

    Returns:
        distance between start and endpoints in km 
    
    '''

    R = 6373.0   #Earth Radius in km
    pi = 3.14159

    lat1 = pi*(minlat/180.0)
    lon1 = pi*(minlon/180.0)
    lat2 = pi*(maxlat/180.0)
    lon2 = pi*(maxlon/180.0)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = 1000*R * c
    
    return(distance)

def xyzout(fname,data,dx,iz,minlon,minlat) :
    ''' Dumps grid depth slice in asci xyz file

    Arguments: 
        fname: Output file name
        data : Binary cube organized as data(z,y,x)
        dx   : Grid interval in x- and y-directions
        iz   : Depth level to dump
        minlon: Longitude origin
        minlat: Lattitude origin
    
    Returns:
        None
'''

    file = open(fname,'w')
    dim=data.shape
    nx=dim[2]
    ny=dim[1]

    nan = np.isnan(data)

    for i in range(0,ny) :
        for j in range(0,nx):
            y=i*dx+minlat
            if nan[iz,i,j] == True:
                print( "===== Nan at: ", i,j)
            x=j*dx+minlon
            file.write(' %f   %f   %f \n' % (x,y,data[iz,i,j]))

    lx = dx*(nx-1)
    ly = dx*(ny-1)
    print ("*** nx,ny: ",nx,ny)
    print ("*** dx:    ",dx)

def intpol3d(ain,d,fac,d3,fac3) :
    ''' Interpolates a regular 3D grid

    Arguments: 
        ain : 3D numpy array. First dimension is depth (z), second dimension is
              lattitude (y), while the third dimension is longitude (x).
        d   : Grid sampling interval in x- and y-directions.
        fac : The output grid sampling interval (dd) is related to the input
              grid sampling (d) by : dd = d/fac
        d3  : Grid sampling interval in the z-direction.
        fac3: The output grid sampling interval (dd3) is related to the input
              grid sampling (d) by : dd3 = d3/fac3
       
    Returns:
        aout: 3D numpy array with grid sampling interval of dd in the
              horizontal directions and dd3 in the vertical direction.
    
    '''

    nz = ain.shape[0]
    ny = ain.shape[1]
    nx = ain.shape[2]
    nnx = int(fac*nx)
    if(ny > 1) :
        nny = int(fac*ny)
    else :
        nny=1
    nnz = int(fac3*nz)
    dd  = d/fac
    dd3  = d3/fac3

    atmp = np.zeros((nz,ny,nnx))
    atmp2 = np.zeros((nz,nny,nnx))
    aout = np.zeros((nnz,nny,nnx))
    
    for i in range(0,nnx) :
        x = i*dd
        ii = int(x/d)
        if(ii < nx-1):
            atmp[:,:,i] = (x-ii*d)*((ain[:,:,ii+1]-ain[:,:,ii])/d) + ain[:,:,ii]
        else:
            atmp[:,:,i] = ain[:,:,nx-1]
    for i in range(0,nny) :
        y = i*dd
        ii = int(y/d)
        if( ii < ny-1) :
            atmp2[:,i,:] = (y-ii*d)*((atmp[:,ii+1,:]-atmp[:,ii,:])/d) + atmp[:,ii,:]
        else: 
            atmp2[:,i,:] = atmp[:,ny-1,:]
    for i in range(0,nnz) :
        z = i*dd3
        ii = int(z/d3)
        if( ii < nz-1) :
            aout[i,:,:] = (z-ii*d3)*((atmp2[ii+1,:,:]-atmp2[ii,:,:])/d3) + atmp2[ii,:,:]
        else: 
            aout[i,:,:] = atmp2[nz-1,:,:]
                
    return(aout) 

def profile(ain, d, xc, yc) :
    ''' Extract a vertical profile defined by surface coordinates xc and yc.
   
    Arguments: 
        ain: 3D numpy array.
        d  : Grid sampling interval in the horizontal directions. 
        xc : List of x-coordinates defining the profile.
        yc : List of y-coordinates defining the profile.

    Returns:
       prof: 2D numpy array of the same lenght as xc (yc). 
             Prof[i,:] contains the interpolated value of
             ain at horisontal position xc[i],yc[i] and at
             all depths.

    '''

    nx=ain.shape[2]
    ny=ain.shape[1]
    nz=ain.shape[0]
    nxc  = xc.shape[0]
    aout = np.zeros((nz,nxc))

    for i in range (0,nxc) :
        x=xc[i]
        y=yc[i]  

        #First find the nearest neighbour grid points to (x,y).
        ix = int(x/d)
        iy = int(y/d)

        # Use bilinear interpolation to find the
        # value at the point (x,y)
        if( iy < ny-1) and (ix < nx-1) :
            k = (ain[:,iy+1,ix]-ain[:,iy,ix])/d
            tmp1 = (y-d*iy)*k+ain[:,iy,ix] 
            k = (ain[:,iy+1,ix+1]-ain[:,iy,ix+1])/d
            tmp2 = (y-d*iy)*k+ain[:,iy,ix] 
            k = (tmp2-tmp1)/d
            aout[:,i] = (x-d*ix)*k+tmp1
        else:
            aout[:,i] = ain[:,iy,ix]

        
    return(aout)   
   

def line(xc, yc, d) :
    ''' Generate coordinates for a straight line 
   

    Arguments: 
        xc : Tuple with x-coordinates of start and end of line
        yc : Tuple with y-coordinates of start and end of line
        d  : Sampling interval along the line

    Returns:
       (xl,yl): Tuple with two arrays containing resampled coordinates
                along the line,
    '''

    X = xc[1]-xc[0]
    Y = yc[1]-yc[0]
    D = sqrt(X**2+Y**2)
    n = int(D/d) + 1
    xl = np.zeros((n))
    yl = np.zeros((n))
    for i in range(0,n) :  
        xl[i] = (d*i)*(X/D)+xc[0]
        yl[i] = (d*i)*(Y/D)+yc[0]
    
    return((xl,yl))                                                                                                            

'''Common plotting functions

This module contains functions for scaling data and plotting

Functions:
    absmax: Return absolute maximum value of numpy array
    norm  : Normalize 2d numpy array
    pclip : Get clip values based on perecntiles
'''

import numpy as np

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

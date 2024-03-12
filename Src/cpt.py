""" Window : window data in a 3D binary cube """

import sys
import argparse
import numpy as N 
import scipy as ML

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def readcpt(name):
	f = open(name,'r')
	lines = f.readlines()
	f.close()
	return lines
	
def gmtcolormap(lines,nColors=None):
	import colorsys
	# f = open('/sw/share/'+ name +'.cpt')
	# Pass already parsed lines rather than a filename
	# so that a default length can be used.
	# lines = f.readlines()
	# f.close()

	x = []
	r = []
	g = []
	b = []
	colorModel = 'RGB'
	for l in lines:
		ls = l.split()
		if l[0] == '#':
		   if ls[-1] == 'HSV':
			   colorModel = 'HSV'
			   continue
		   else:
			   continue
		if ls[0] == 'B' or ls[0] == 'F' or ls[0] == 'N':
		   pass
		else:
			x.append(float(ls[0]))
			r.append(float(ls[1]))
			g.append(float(ls[2]))
			b.append(float(ls[3]))
			xtemp = float(ls[4])
			rtemp = float(ls[5])
			gtemp = float(ls[6])
			btemp = float(ls[7])
		
	x.append(xtemp)
	r.append(rtemp)
	g.append(gtemp)
	b.append(btemp)

	nTable = len(r)	   
	x = N.array( x , N.single)
	r = N.array( r , N.single)
	g = N.array( g , N.single)
	b = N.array( b , N.single)
	xmin = x[0]
	rangeOfX = x[-1] - x[0]
	x = (x - xmin)/rangeOfX
	
	# How long will the new colormap be?
	if not nColors:
		nColors = len(r)
	
	xx = ML.linspace(x[0], x[-1], nColors)
	xx = N.array( xx, N.single)
	if colorModel == 'HSV':
	   for i in range(r.shape[0]):
		   rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
		   r[i] = rr ; g[i] = gg ; b[i] = bb

	rxx = xx*0.0
	gxx = xx*0.0
	bxx = xx*0.0
	for i in range(nColors):
		j = N.searchsorted(x,xx[i])
		if j == 0:
			rxx[i] = r[0] ; gxx[i] = g[0] ;bxx[i] = b[0]
		elif j == x.shape[0]:
			rxx[i] = r[-1] ; gxx[i] = g[-1] ;bxx[i] = b[-1]
		else:
			rxx[i] = r[j-1] + (r[j] - r[j-1])*(xx[i]-x[j-1])/(x[j]-x[j-1])
			gxx[i] = g[j-1] + (g[j] - g[j-1])*(xx[i]-x[j-1])/(x[j]-x[j-1])
			bxx[i] = b[j-1] + (b[j] - b[j-1])*(xx[i]-x[j-1])/(x[j]-x[j-1])
			
	# This was originally written for Matlab which wants rgb in 
	# 0.0-1.0, NCL uses 0-255
	#if colorModel == 'RGB':
		#rxx = rxx/255.
		#gxx = gxx/255.
		#bxx = bxx/255.
		
	rxx = rxx.tolist()
	gxx = gxx.tolist()
	bxx = bxx.tolist()
		
	return (rxx, gxx, bxx)

def getcpt(file) :
  cpt = readcpt(file)
  ncol=127
  r,g,b = gmtcolormap(cpt,ncol)

  n=len(r)
  list = N.zeros((n,4))
  for i in range(0,n) :
    list[i,0] = r[i]/255.0
    list[i,1] = g[i]/255.0
    list[i,2] = b[i]/255.0
    list[i,3] = 1.0
  return(list)




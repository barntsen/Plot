#!/bin/sh

abpsource -n 501 -d 0.002  -m 1.0 -f 15.0 -t 0.150 -o pulse.bin
graph -n1 501 -n2 1 pulse.bin 
resamp -n1 501 -n2 1 -d1 0.002 -d1out 0.0005 pulse.bin wavelet.bin
graph -n1 2001 -n2 1 wavelet.bin 

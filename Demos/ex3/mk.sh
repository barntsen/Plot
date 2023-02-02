#!/bin/sh
./clean.sh
movie   -d1 10.0 \
        -d2 10.0 \
        -xlabel "Distance (km)" \
        -ylabel "Depth (km)"    \
        -pclip 99.0    \
        -fbg  cp.bin   \
        -o snp.mp4     \
        -ar 2.0        \
        -n1 500        \
        -n2 100        \
        -n3 150        \
        snp.bin

#!/bin/sh
./clean.sh

image -ar 2                     \
      -title "Sigsbee Vp (m/s)" \
      -xlabel "Distance (km)"   \
      -ylabel "Depth (km)"      \
      -cmin 1450                \
      -cmax 4600                \
      -colorbar -o vp.pdf       \
      -d1 0.0762                \
      -d2 0.0762                \
      -n1 3201                  \
      -n2 1201                  \
      -colormap jet             \
      cp.bin

window -n1 16000 \
       -n2 1001  \
       -f1 0     \
       -l1 16000 \
       -f2 0     \
       -l2 1001  \
       -i2 4     \
       -i1 8     \
       data.bin xaa.bin

transp n1=2000 <xaa.bin >xab.bin

image  -pclip 98.0             \
       -o data.pdf             \
       -xlabel "Distance (km)" \
       -ylabel "Time (sec)"    \
       -d1 0.030               \
       -d2 0.008               \
       -n2 2000                \
       -n1 251                 \
       xab.bin

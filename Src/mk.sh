#!/bin/sh

EXE=\#\!/usr/bin/python3
echo $EXE > xaa.txt
inst=../Bin

cat xaa.txt ricker.py > $inst/ricker
chmod +x $inst/ricker
cat xaa.txt spike.py  > $inst/spike
chmod +x $inst/spike
cat xaa.txt  window.py > $inst/window
chmod +x $inst/window
cat xaa.txt reverse.py > $inst/reverse
chmod +x $inst/reverse
cat xaa.txt resamp.py > $inst/resamp
chmod +x $inst/resamp
cat xaa.txt pad.py > $inst/pad
chmod +x $inst/pad
cat xaa.txt scale.py > $inst/scale
chmod +x $inst/scale
cat xaa.txt integrate.py > $inst/integrate
chmod +x $inst/integrate
cat xaa.txt der.py > $inst/der
chmod +x $inst/der
cat xaa.txt spec.py > $inst/spec
chmod +x $inst/spec
cat xaa.txt rms.py > $inst/rms
chmod +x $inst/rms
cat xaa.txt rms2.py > $inst/rms2
chmod +x $inst/rms2
cat xaa.txt minerr.py > $inst/minerr
chmod +x $inst/minerr
cat xaa.txt cross.py > $inst/cross
chmod +x $inst/cross
cat xaa.txt energy.py > $inst/energy
chmod +x $inst/energy
cat xaa.txt ricker.py > $inst/ricker
chmod +x $inst/ricker
cat xaa.txt add.py > $inst/add
chmod +x $inst/add
cat xaa.txt wiggle.py > $inst/wiggle
chmod +x $inst/wiggle
cat xaa.txt graph.py > $inst/graph
chmod +x $inst/graph
cat xaa.txt image.py > $inst/image
chmod +x $inst/image
cat xaa.txt movie.py > $inst/movie
chmod +x $inst/movie
cat xaa.txt graphxy.py > $inst/graphxy
chmod +x $inst/graphxy
cat xaa.txt fdecon.py > $inst/fdecon
chmod +x $inst/fdecon
cat xaa.txt conv.py > $inst/conv
chmod +x $inst/conv
cat xaa.txt dcrem.py > $inst/dcrem
chmod +x $inst/dcrem
cat xaa.txt b2a.py > $inst/b2a
chmod +x $inst/b2a

cp parula.py $inst
cp pltcom.py $inst
cp parula.py $inst
cp pltcom.py $inst
cp pltcom.py $inst
cp babin.py $inst 
cp barsf.py $inst 
cp bacolmaps.py $inst
cp rss.py  $inst
cp cpt.py   $inst

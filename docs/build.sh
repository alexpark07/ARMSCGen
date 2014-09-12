#!/bin/sh
#rm -rf apidoc
sphinx-apidoc -F -f -o apidoc -H ARMSCGen -A alex.park ../
#sphinx-apidoc -F -f -o apidoc -H ARMSCGen -A alex.park -V `cat ../VERSION.txt` ../
#cd apidoc
#make html

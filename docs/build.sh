#!/bin/sh
rm -rf apidoc
sphinx-apidoc -F -f -o apidoc -H ARMSCGen -A alex.park ../
#cd apidoc
#make html

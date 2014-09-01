#!/bin/sh
sphinx-apidoc -F -f -o apidoc ../
cd apidoc
make html

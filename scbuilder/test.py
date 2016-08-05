#!/usr/bin/env python

import scbuilder

th = scbuilder.THUMB()
print th.execve('/bin/sh', 1)

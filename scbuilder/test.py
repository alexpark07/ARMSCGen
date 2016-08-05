#!/usr/bin/env python

import scbuilder

th = scbuilder.THUMB()
a2t = th.arm_to_thumb()
dup2 = th.dup2(4)
execve = th.execve('/bin/sh')
exit = th.exit()
#print a2t + dup2 + execve
print a2t + exit

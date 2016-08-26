#!/usr/bin/env python

import os, sys

HEAD = """.global _start
.section .text

_start:
"""

THUMB = """.arm
add r6, pc, #1
bx r6
.thumb
"""

def parse(arch, code):
    print HEAD
    if arch == 'thumb':
        print THUMB
    
    print code

    if arch == 'thumb':
        sys.stderr.write("as fn.s -o fn.o -mthumb\n")
    else:
        sys.stderr.write("as fn.s -o fn.o\n")

    sys.stderr.write("ld fn.o -o fn\n")
        

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Usage: %s [thumb|arm]" % sys.argv[0]
        sys.exit(0)

    dat = ''
    for i in sys.stdin:
        dat += i

    parse(sys.argv[1], dat)

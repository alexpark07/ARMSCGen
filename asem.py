#!/usr/bin/env python2

import os, sys
import tempfile
from optparse import OptionParser

OBJDUMP = 'arm-linux-gnueabi-objdump'
OBJCOPY = 'arm-linux-gnueabi-objcopy'
AS      = 'arm-linux-gnueabi-as'

ARM64_OBJDUMP = 'aarch64-linux-gnu-objdump'
ARM64_OBJCOPY = 'aarch64-linux-gnu-objcyop'
ARM64_AS      = 'aarch64-linux-gnu-as'

g_arch    = 'i386'
g_format  = 'string'
g_discode = False

def _string(s):
    out = []
    for c in s:
        co = ord(c)
        out.append('\\x%02x' % co)
    return '"' + ''.join(out) + '"\n'

def _carray(s):
    out = []
    for c in s:
        out.append('0x' + enhex(c))
    return '{' + ', '.join(out) + '};\n'

def enhex(c):
    return c.encode('hex')

def unhex(c):
    return c.decode('hex')

def compile(fn):
    if g_arch == "arm":
        cmd = '%s %s.s -o %s.o' % (AS, fn, fn)
    elif g_arch == "thumb":
        cmd = '%s %s.s -o %s.o -mthumb' % (AS, fn, fn)
    elif g_arch == "arm64":
        cmd = '%s %s.s -o %s.o' % (ARM64_AS, fn, fn)
    elif g_arch == "i386":
        cmd = 'as %s.s -o %s.o --32' % (fn, fn)
    elif g_arch == "amd64":
        cmd = 'as %s.s -o %s.o --64' % (fn, fn)
    os.system(cmd)
    if os.path.exists('%s.o' % (fn)) == False:
        print "There is no result: as"
        return -1

    tempfn = '%s.tmp1' % (fn)
    if (g_arch == 'i386') or (g_arch == 'amd64'):
        cmd = 'objcopy -j.text -Obinary %s.o %s' % (fn, tempfn)
    elif (g_arch == 'arm') or (g_arch == 'thumb'):
        cmd = '%s -j.text -Obinary %s.o %s' % (OBJCOPY, fn, tempfn)
    elif (g_arch == 'arm64'):
        cmd = '%s -j.text -Obinary %s.o %s' % (ARM64_OBJCOPY, fn, tempfn)
    else:
        print "What kind of arch do you want to use"
        return -1

    os.system(cmd)
    if os.path.exists(tempfn) == False:
        print "There is no result: objdump"
        return -1

    f = open(tempfn, 'rb').read()

    if g_format == 'c':
        print _carray(f)
    elif g_format == 'string':
        print _string(f)
    elif g_format == 'raw':
        print f
    elif g_format == 'hex':
        print enhex(f)
    else:
        print _string(f)

    if os.path.exists(tempfn):
        os.unlink(tempfn)

    if os.path.exists('%s.o' % (fn)):
        os.unlink('%s.o' % (fn))

    return 0

def asm_src(msg, fn, mode):
    SRC = '''
.section .text
.globl _start
_start:
    %s
    %s
''' % (mode, msg.replace(';', '\n'))
    try:
        open('%s.s' % (fn), 'w').write(SRC)
    except:
        print "Failed to create .asm source file"
        return -1

    compile(fn)

def AsmCode(msg, fn):
    if g_arch == 'i386':
        asm_src(msg, fn, '')
    elif g_arch == 'amd64':
        asm_src(msg, fn, '')
    elif g_arch == 'arm' or g_arch == 'arm64':
        asm_src(msg, fn, '.arm')
    elif g_arch == 'thumb':
        asm_src(msg, fn, '.thumb')
    else:
        return -1

def DisCode(msg, fn):
    tempfn = '%s.tmp1' % (fn)
    if g_arch == 'i386':
        opt = 'objdump %s -D -b binary -mi386 -Mintel > %s' % (fn, tempfn)
    elif g_arch == 'amd64':
        opt = 'objdump -D -b binary -mi386:x86-64 -Mintel %s > %s' % (fn, tempfn)
    elif g_arch == 'arm':
        opt = '%s -D -b binary -marm %s > %s' % (OBJDUMP, fn, tempfn)
    elif g_arch == 'thumb':
        opt = '%s -D -b binary -marm -Mforce-thumb %s > %s' % (OBJDUMP, fn, tempfn)
    elif g_arch == 'arm64':
        opt = '%s -D -b binary -maarch64 %s > %s' % (ARM64_OBJDUMP, fn, tempfn)
    else:
        return -1

    try:
        open(fn, 'wb').write(msg)
    except:
        print "Failed to create a file: %s" % (fn)
        return -1

    rv = os.popen(opt).read()
    if os.path.exists(tempfn) == False:
        print "There is no result"
        os.unlink(tempfn)
        return -1

    f = open(tempfn, 'r').readlines()

    flag = 0
    for v in f:
        if flag == 1:
            print v.strip()
        if flag == 0:
            if v.find('<.data>:') != -1:
                flag = 1

    if os.path.exists(tempfn):
        os.unlink(tempfn)

    return 0


if __name__ == '__main__':
    parser = OptionParser(description = 'asm/disasm code by alex.park')
    parser.add_option('-a', '--architechture',
                   dest='arch',
                   type = str,
                   help = 'options: thumb, arm, arm64(aarch64), i386, amd64 (default: i386)')

    parser.add_option('-f', '--format',
                   dest = 'format',
                   type = 'choice',
                   choices = ['r', 'raw',
                              's', 'str', 'string',
                              'h', 'hex',
                              'c'
                             ],
                   help = '{r}aw, {s}tring, {h}ex, {c} for C code if encoded',
                   ) 

    parser.add_option('-d', '--disassemble',
                   dest='discode',
                   action = 'store_true'
                   )

    (opt, args) = parser.parse_args()

    if opt.arch:
        g_arch = opt.arch

    if opt.format:
        if opt.format in ['r', 'raw']:
            g_format = 'raw'
        elif opt.format in ['s', 'str', 'string']:
            g_format = 'string'
        elif opt.format == 'c':
            g_format = 'c'
        elif opt.format in ['h', 'hex']:
            g_format = 'hex'
        else:
            g_format = 'string'

    if opt.discode:
        g_discode = True

    data = sys.stdin.read()
    fn = tempfile.mktemp()

    if g_discode == True:
        DisCode(data, fn)
    else:
        AsmCode(data, fn)

    if os.path.exists(fn):
        os.unlink(fn)


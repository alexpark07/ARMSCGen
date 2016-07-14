#!/usr/bin/env python2

import os, sys
import tempfile
from optparse import OptionParser
from struct import unpack, pack

g_arch     = 'i386'
g_format   = 'string'
g_discode  = False
g_capstone = True
g_keystone = True

try:
    from keystone import *
except ImportError:
    g_keystone = False

try:
    from capstone import *
    from capstone.arm import *
except ImportError:
    g_capstone = False

'''
if keystone / capstone are not installed then we need to GNU Tools
'''
OBJDUMP       = 'objdump'
OBJCOPY       = 'objcopy'
AS            = 'as'

ARM32_OBJDUMP = 'arm-linux-gnueabi-objdump'
ARM32_OBJCOPY = 'arm-linux-gnueabi-objcopy'
ARM32_AS      = 'arm-linux-gnueabi-as'

ARM64_OBJDUMP = 'aarch64-linux-gnu-objdump'
ARM64_OBJCOPY = 'aarch64-linux-gnu-objcopy'
ARM64_AS      = 'aarch64-linux-gnu-as'

def u8(u, rep=1):
    return unpack(('<' + 'c'*rep), u)

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

def pprint(f):
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

    return

def compile(fn):
    if g_arch == "arm":
        cmd = '%s %s.s -o %s.o' % (ARM32_AS, fn, fn)
    elif g_arch == "thumb":
        cmd = '%s %s.s -o %s.o -mthumb' % (ARM32_AS, fn, fn)
    elif g_arch == "arm64":
        cmd = '%s %s.s -o %s.o' % (ARM64_AS, fn, fn)
    elif g_arch == "i386":
        cmd = '%s %s.s -o %s.o --32' % (AS, fn, fn)
    elif g_arch == "amd64":
        cmd = '%s %s.s -o %s.o --64' % (AS, fn, fn)
    os.system(cmd)
    if os.path.exists('%s.o' % (fn)) == False:
        print "There is no result: as"
        return -1

    tempfn = '%s.tmp1' % (fn)
    if (g_arch == 'i386') or (g_arch == 'amd64'):
        cmd = '%s -j.text -Obinary %s.o %s' % (OBJCOPY, fn, tempfn)
    elif (g_arch == 'arm') or (g_arch == 'thumb'):
        cmd = '%s -j.text -Obinary %s.o %s' % (ARM32_OBJCOPY, fn, tempfn)
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
    pprint(f)

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
    if g_arch == 'arm':
        asm_src(msg, fn, '.arm')
    elif g_arch == 'thumb':
        asm_src(msg, fn, '.thumb')
    else:
        asm_src(msg, fn, '')

def AsmCodeWithKS(msg):
    ks_arch = ''
    ks_mode = ''
    if g_arch == "arm":
        ks_arch = KS_ARCH_ARM
        ks_mode = KS_MODE_ARM
    elif g_arch == "thumb":
        ks_arch = KS_ARCH_ARM
        ks_mode = KS_MODE_THUMB
    elif g_arch == "arm64":
        ks_arch = KS_ARCH_ARM64
        ks_mode = KS_MODE_LITTLE_ENDIAN
    elif g_arch == "i386":
        ks_arch = KS_ARCH_X86
        ks_mode = KS_MODE_32
    elif g_arch == "amd64":
        ks_arch = KS_ARCH_X86
        ks_mode = KS_MODE_64

    ks = Ks(ks_arch, ks_mode)

    f, count = ks.asm(msg)

    dat = ''
    for v in f:
        dat += chr(v)

    pprint(dat)

def DisCode(msg, fn):
    tempfn = '%s.tmp1' % (fn)
    if g_arch == 'i386':
        opt = '%s %s -D -b binary -mi386 -Mintel > %s' % (OBJDUMP, fn, tempfn)
    elif g_arch == 'amd64':
        opt = '%s -D -b binary -mi386:x86-64 -Mintel %s > %s' % (OBJDUMP, fn, tempfn)
    elif g_arch == 'arm':
        opt = '%s -D -b binary -marm %s > %s' % (ARM32_OBJDUMP, fn, tempfn)
    elif g_arch == 'thumb':
        opt = '%s -D -b binary -marm -Mforce-thumb %s > %s' % (ARM32_OBJDUMP, fn, tempfn)
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

def DisCodeWithCS(msg):

    data = msg

    if g_arch == 'arm':
        xarch = CS_ARCH_ARM
        xmode = CS_MODE_ARM
    elif g_arch == 'arm64':
        xarch = CS_ARCH_ARM64
        xmode = CS_MODE_ARM
    elif g_arch == 'thumb':
        xarch = CS_ARCH_ARM
        xmode = CS_MODE_THUMB
    elif g_arch == 'i386':
        xarch = CS_ARCH_X86
        xmode = CS_MODE_32
    elif g_arch == 'amd64':
        xarch = CS_ARCH_X86
        xmode = CS_MODE_64
    else:
        print "Not supports arch for you yet"
        sys.exit(-1)

    md = Cs(xarch, xmode)
    md.detail = True
    totalSize = 0
    dat = ''
    fmtstr = ''
    if g_arch == 'arm' or g_arch == 'arm64' or g_arch == 'thumb':
        fmtstr = "0x%08x (%04d): %-13s %-8s %s\n"
    elif g_arch == 'i386':
        fmtstr = "0x%08x (%04d): %-21s %-8s %s\n"
    else:
        fmtstr = "0x%08x (%04d): %-31s %-8s %s\n"

    for i in md.disasm(data, 0x0000):
        if i.size:
            _tmp = []
            for _x in u8(i.bytes, i.size):
                _tmp.append(_x.encode('hex'))
            s = "%s" % ' '.join(_tmp)
        else:
            s = -1

        dat += fmtstr % (i.address, totalSize, s, i.mnemonic, i.op_str)
        totalSize += i.size
    print dat

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
    fn = ''
    if g_discode == True:
        if g_capstone == True:
            DisCodeWithCS(data)
        else:
            fn = tempfile.mktemp()
            DisCode(data, fn)
    else:
        if g_keystone == True:
            AsmCodeWithKS(data)
        else:
            fn = tempfile.mktemp()
            AsmCode(data, fn)

    if os.path.exists(fn):
        os.unlink(fn)


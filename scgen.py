#!/usr/bin/python2

from optparse import OptionParser
import sys
import os

from ARMSCGen import *

thgen    = thumbSCGen()
armgen   = armSCGen()
arm64gen = arm64SCGen()

g_arch      = 'thumb'
g_shellcode = ''
g_format    = 'asm'
g_xorkey    = False
g_testSC    = False

# pwntools from pwnies
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

def isScode(s, sname):
    d = {}
    rv = {}
    for v in dir(s):
        if len(v) == 0:
            continue
        if v[0] == '_':
            continue
        d[v] = (eval("%s.%s" % (sname, v)))
    rv[sname] = d
    return rv

def getShellcodeNames(scs, arch='all'):
    _scname = ''
    xscname = {'thgen':'thumb', 'armgen':'arm', 'arm64gen':'arm64'}

    for i in range(0, len(scs)):
        scname = scs[i].keys()[0]
        _scname = xscname[scname]
        if arch != 'all':
            if _scname != arch:
                continue
                
        sckeys = scs[i][scname].keys()
        sckeys.sort()
        print "=" * 40
        print "### architechture: %s - total(%02d)" % (_scname, len(sckeys))
        print "=" * 40
        for sc in sckeys:
            print "``" + sc + "``"

        print ""

def showShellcode(args):
    try:
        if g_arch == 'arm':
            show = eval("armgen.%s.__doc__" % (args[0]))
        elif g_arch == 'arm64':
            show = eval("arm64gen.%s.__doc__" % (args[0]))
        elif g_arch == 'thumb':
            show = eval("thgen.%s.__doc__" % (args[0]))
    except AttributeError:
        show = "There is no '%s' shellcode so far" % (args[0])
    except:
        show = "Unknown execption"

    print "=" * 80
    print "%s" % (show)
    print "=" * 80
    sys.exit(-1)


def genShellcode(args):
    fms = []
    for i in range(0, len(args)):
        fms.append( "'%s'" % (args[i]) )

    scode = fms[0].replace("'", "") + "(" + ','.join(fms[1:]) + ")"
    scode_tc = fms[0].replace("'", "") + "_tc(" + ','.join(fms[1:]) + ")"

    try:
        if g_arch == 'arm':
            show = eval("armgen.%s" % (scode))
            prepareCompiler('ARM')
        elif g_arch == 'arm64':
            show = eval("arm64gen.%s" % (scode))
            prepareCompiler('ARM64')
        elif g_arch == 'thumb':
            show = eval("thgen.%s" % (scode))
            prepareCompiler('THUMB')

        if g_format == 'asm':
            print show
            if g_testSC == False:
                return

        if g_arch == 'thumb':
            scode = CompileSC(show, isThumb=True)
        else:
            scode = CompileSC(show)

        if g_xorkey == True:
            if g_arch == 'thumb':
                scode = MakeXorShellcode( scode )

        if g_testSC == True:
            if g_arch == 'arm':
                eval("armgen.%s" % (scode_tc))
            elif g_arch == 'arm64':
                eval("arm64gen.%s" % (scode_tc))
            elif g_arch == 'thumb':
                eval("thgen.%s" % (scode_tc))

        if g_format == 'asm': 
            return

        if g_format == 'c':
            print _carray(scode)
        elif g_format == 'string':
            print _string(scode)
        elif g_format == 'raw':
            print scode
        elif g_format == 'hex':
            print enhex(scode)
        elif g_format == 'python':
            _xscode = []
            _xscode.append('shellcode = ""\n')
            _xdiv = len(scode) / (16)
            _xmod = len(scode) % (16)
            _x = 0
            for _i in range(0, _xdiv):
                _xscode.append('shellcode += %s' % _string(scode[_i*16:(_i+1)*16]))
                _x = _x + 1
            if _xmod:
                _xscode.append('shellcode += %s' % _string(scode[(_i+1)*16:]))
            print "# shellcode's length is : %s" % (len(scode))
            print ''.join(_xscode)

        else:
            print _string(scode)

    except AttributeError:
        print "There is no '%s' shellcode so far" % (args[0])
    except:
        show = "I think, you have wrong options. show shellcode for you"
        print show
        showShellcode(args)

if __name__ == '__main__':

    scs = []
    scs.append(isScode(thgen,    'thgen'))
    scs.append(isScode(armgen,   'armgen'))
    scs.append(isScode(arm64gen, 'arm64gen'))

    parser = OptionParser(description = 'ARM32/64 shellcodes by alex.park')
    parser.add_option('-a', '--architechture',
                   dest='arch',
                   type = str,
                   help = 'ARM Archtechture (default: arm32 thumb) options: thumb, arm, arm64')
    parser.add_option('-?', '--show',
                   action = 'store_true',
                   help = 'Show shellcode documentation',
                   )
    parser.add_option('-l', '--list',
                   action = 'store_true',
                   help = 'List all the shellcodes if arch is "all"',
                   )
    parser.add_option('-f', '--format',
                   dest = 'format',
                   type = 'choice',
                   choices = ['r', 'raw',
                              's', 'str', 'string',
                              'h', 'hex',
                              'a', 'asm', 
                              'c',
                              'p', 'py', 'python',
                             ],
                   help = '{r}aw, {s}tring, {h}ex, {a}sm, {c} for C code, {p|py}thon for python code',
                   )
    parser.add_option('-x', '--xor',
                  dest = 'xor',
                  action="store_true",
                  default = False,
                  help = 'XOR Encoder if you want to avoid bad chars like 0x00, 0x0a and so on\nNotice: only for arm32, thumb shellcodes so far',
                  )

    parser.add_option('-t', '--test',
                  dest = 'testSC',
                  action="store_true",
                  default = False,
                  help = 'Shellcode Test in unicorn engine'
                  )

    (opt, args) = parser.parse_args()

    if opt.arch:
        g_arch = opt.arch

    if opt.list and opt.show:
        print "Which shellcode do you want to read show()"
        sys.exit(-1)

    if opt.list:
        getShellcodeNames(scs, arch=g_arch)
        sys.exit(-1)

    if opt.show:
        if len(args) == 0:
            print "Please choice one of shellcodes to show you"
            sys.exit(-1)
        showShellcode(args)
        sys.exit(-1)

    if opt.format:
        if opt.format in ['r', 'raw']:
            g_format = 'raw'
        elif opt.format in ['s', 'str', 'string']:
            g_format = 'string'
        elif opt.format in ['a', 'asm']:
            g_format = 'asm'
        elif opt.format == 'c':
            g_format = 'c'
        elif opt.format in ['h', 'hex']:
            g_format = 'hex'
        elif opt.format in ['p', 'py', 'python' ]:
            g_format = 'python'
        else:
            g_format = 'asm'

    if opt.xor:
        g_xorkey = True

    if opt.testSC:
        g_testSC = True

    if len(args) == 0:
        print "Please choice one of shellcodes to show you"
        print parser.print_help()
        sys.exit(-1)

    else:
        genShellcode(args)

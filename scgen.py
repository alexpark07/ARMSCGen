#!python

from optparse import OptionParser
import sys
import os

from ARMSCGen import *

thgen    = thumbSCGen()
armgen   = armSCGen()
arm64gen = arm64SCGen()

g_arch = 'thumb'
g_shellcode = ''

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
    if isinstance(c, int) == True:
        c = str(c)
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

def getShellcodeNames(scs, arch='*'):
    _scname = ''

    for i in range(0, len(scs)):
        scname = scs[i].keys()[0]
        if arch != '*':
            if scname ==   'thgen':
                _scname =  'thumb'
            elif scname == 'armgen':
                _scname =  'arm'
            elif scname == 'arm64gen':
                _scname =  'arm64'
            else:
                _scname =  'thumb'

            if _scname != arch:
                continue
                
        sckeys = scs[i][scname].keys()
        sckeys.sort()
        print "=" * 40
        print "architechture: %s - total(%02d)" % (_scname, len(sckeys))
        print "=" * 40
        for sc in sckeys:
            print sc

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
        fms.append( "%s" % (args[i]) )

    scode = fms[0] + "(" + ','.join(fms[1:]) + ")"

    try:
        if g_arch == 'arm':
            show = eval("armgen.%s" % (scode))
        elif g_arch == 'arm64':
            show = eval("arm64gen.%s" % (scode))
        elif g_arch == 'thumb':
            show = eval("thgen.%s" % (scode))
    except AttributeError:
        show = "There is no '%s' shellcode so far" % (args[0])
    except:
        show = "I think, you have wrong options. show shellcode for you"
        print show
        showShellcode(args)

    print show

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
                   help = 'List all the shellcodes',
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


    if len(args) == 0:
        print "Please choice one of shellcodes to show you"
        print parser.print_help()
        sys.exit(-1)

    else:
        genShellcode(args)

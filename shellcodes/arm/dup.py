# dup() in ARM Mode
def generate(sock=4):
    sc = """
    mov r9, #%s
    mov r8, #2
loop_2:
    mov r0, r9
    mov r1, r8
    svc (0x900000+ 63)
    adds r8, #-1
bpl loop_2
    """ % (sock)

    return sc

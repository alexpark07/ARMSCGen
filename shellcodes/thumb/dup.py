# dup(sock)
def generate(sock=4):
    sc = """
    mov r1, #3
    mov r7, #(0+ 63)
    sub r2, r2, r2
    """
    if isinstance(sock, int):
        sc += 'mov r5, #%s' % (sock)
    else:
        sc += 'mov r5, %s' % (sock)
    sc += """
loop_2:
    mov r0, r5
    sub r1, r1, #1
    svc 1
    cmp r1, r2
    bne loop_2
    """
    return sc

def generate(sock=4):
    """Duplicates sock to stdin, stdout and stderr

    Args:
        sock(int/str/reg): sock descriptor

    """
    sc = """
    mov x20, %s
    mov x21, 2
loop_1:
    mov x0, x20 
    mov x1, x21 
    sub x2, x2, x2
    mov x8, 24 
    svc 0
    sub x21, x21, 1
    cmp x21, -1
    bne loop_1
    """ % (sock)
    return sc

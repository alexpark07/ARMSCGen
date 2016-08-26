# getdents syscall

def generate(in_fd):
    """getdents - lists specific directory in thumb mode

    Args: 
        in_fd - (int/str/reg): in file descriptor 
    """

    sc = ''
    try:
        xin_fd = int(in_fd)
        sc += 'movs r0, #%s' % (xin_fd)
    except:
        sc += 'movs r0, %s' % (in_fd)

    sc += """
    mov  r1, sp
    movs r2, #255
    movs r7, #141
    svc 1
    """
    return sc

# getdents syscall

def generate(in_fd):
    """getdents - lists specific directory

    Args: 
        in_fd - (int/str/reg): in file descriptor 
    """

    sc = ''
    try:
        xin_fd = int(in_fd)
        sc += 'mov r0, #%s' % (xin_fd)
    except:
        sc += 'mov r0, %s' % (in_fd)

    sc += """
    mov r1, sp
    mov r2, #255
    mov r7, #141
    svc 0
    """
    return sc

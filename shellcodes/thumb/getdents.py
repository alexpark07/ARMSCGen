# getdents syscall

def generate(in_fd):
    """getdents - lists specific directory in thumb mode

    argument: 
        in_fd - (int/str/reg): in file descriptor 
    """

    if isinstance(in_fd, int) == True:
        sc = "mov r0, #%s" % (in_fd)
    else:
        sc = "mov r0, %s" % (in_fd)

    sc += """
    mov r1, sp
    mov r2, #255
    mov r7, #141
    svc 1
    """
    return sc

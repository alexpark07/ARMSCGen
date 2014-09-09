# getdents syscall

def generate(in_fd):
    """getdents - lists specific directory

    argument: 
        in_fd - (int/str/reg): in file descriptor 
    """

    sc = """
    mov x0, %s
    mov x1, sp
    mov x2, #255
    mov x8, #61
    svc 1
    """ % (in_fd)
    return sc

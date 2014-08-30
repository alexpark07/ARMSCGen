# read from stack and write to file descriptor

def generate(out_fd, size):
    """Writes a file from stack in thumb mode
    
    Args: 
        out_fd (imm/reg)        = file descriptor
        size (int/str/imm/reg)  = 255
    """

    if isinstance(size, int) == True:
        sc = "mov r2, #%s" % int(size)
    else:
        sc = "mov r2, %s" % (size)

    sc += """
    mov r0, #%s
    mov r1, sp
    mov r7, #4
    svc 1
    """ % (out_fd)
    return sc

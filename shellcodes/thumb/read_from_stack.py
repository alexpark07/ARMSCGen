# read from stack and write to file descriptor

def generate(out_fd, size):
    """Writes a file from stack in thumb mode
    
    argument: 
        out_fd (int/str/reg) = file descriptor
        size   (int/str/reg) = size to read
    """

    if isinstance(out_fd, int) == True:
        xout_fd = "#%s" % int(out_fd)
    else:
        xout_fd = out_fd

    if isinstance(size, int) == True:
        xsize = "#%s" % int(size)
    else:
        xsize = size

    sc = """
    mov r2, %s
    mov r0, %s
    mov r1, sp
    mov r7, #4
    svc 1
    """ % (xsize, xout_fd)
    return sc

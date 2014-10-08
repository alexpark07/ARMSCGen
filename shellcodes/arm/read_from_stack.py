# read from stack and write to file descriptor

def generate(out_fd, size):
    """Writes a file from stack
    
    Args: 
        out_fd (int/str/reg) = file descriptor

        size   (int/str/reg) = size to read
    """

    try:
        xout_fd = '#%s' % int(out_fd)
    except:
        xout_fd = '%s' % out_fd

    try:
        xsize = '#%s' % int(size)
    except:
        xsize = '%s' % size

    sc = """
    mov r2, %s
    mov r0, %s
    mov r1, sp
    mov r7, #4
    svc 0
    """ % (xsize, xout_fd)
    return sc

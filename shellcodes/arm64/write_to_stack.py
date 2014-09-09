# read from file descriptor and write to stack

def align4(n):
    m = n / 4
    return 4 * (m+1)

def align8(n):
    m = n / 8
    return 8 * (m+1)

def generate(in_fd, size):
    """Writes data to stack
    
    Args: 
        in_fd (int/str/reg) = file descriptor

        size  (int/str/reg) = size to write
    """

    if isinstance(size, int) == True:
        xsize = "%s" % align8(size)
    else:
        xsize = size

    sc = """
    sub sp, %s
    mov x0, %s
    mov x2, %s
    mov x1, sp
    mov x8, 63
    svc 1
    """ % (xsize, in_fd, xsize)

    return sc

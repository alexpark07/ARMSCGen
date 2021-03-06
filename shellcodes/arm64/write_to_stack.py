# read from file descriptor and write to stack

def align4(n):
    m = n / 4
    x = n % 4
    if x == 0:
        return n
    return 4 * (m+1)

def align8(n):
    m = n / 8
    x = n % 8
    if x == 0:
        return n
    return 8 * (m+1)

def generate(in_fd, size):
    """Writes data to stack
    
    Args: 
        in_fd (int/str/reg) = file descriptor

        size  (int/str/reg) = size to write
    """

    try:
        xsize = int(size)
        xsize = "%s" % align8(xsize)
    except:
        xsize = size

    sc = """
    sub sp, sp, %s
    mov x0, %s
    mov x2, %s
    mov x1, sp
    mov x8, 63
    svc 1
    """ % (xsize, in_fd, xsize)

    return sc

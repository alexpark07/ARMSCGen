# read from file descriptor and write to stack


def align4(n):
    m = n / 4
    return 4 * (m+1)

def generate(in_fd, size):
    """Writes data to stack in thumb mode
    
    Args: 
        in_fd (int/str/reg) = file descriptor
        size  (int/str/reg) = size to write
    """

    try:
        xin_fd = "#%s" % int(in_fd)
    except:
        xin_fd = in_fd

    try:
        size = int(size)
        xsize = "#%s" % align4(size)
    except:
        xsize = size

    sc = """
    sub sp, %s
    mov r0, %s
    mov r2, %s
    mov r1, sp
    mov r7, #3
    svc 1
    """ % (xsize, xin_fd, xsize)

    return sc

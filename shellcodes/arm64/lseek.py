# lseek with file descriptor

SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

def generate(out_fd, offset=0, whence=SEEK_END):
    """lseek3264 with file descriptor
    
    Args: 
        out_fd (int/str/reg) = file descriptor

        offset (int/str/reg) = offset 

        whence (int/enum) = position depends on offset
    """

    sc = """
    /* lseek(...) */
    mov x0, %s
    mov x1, %s
    mov x2, %s
    mov x8,62 
    svc 1
    """ % (out_fd, offset, whence)
    return sc

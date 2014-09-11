# fsync with file descriptor

def generate(out_fd):
    """fsync with file descriptor
    
    Args: 
        out_fd (int/str/reg) = file descriptor
    """

    sc = """
    /* fsync(...) */
    mov x0, %s
    mov x8, 82
    svc 1
    """ % (out_fd)
    return sc

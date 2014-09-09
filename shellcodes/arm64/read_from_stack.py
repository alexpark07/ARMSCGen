# read from stack and write to file descriptor

def generate(out_fd, size):
    """Writes a file from stack
    
    argument: 
        out_fd (int/str/reg) = file descriptor
        size   (int/str/reg) = size to read
    """

    sc = """
    mov x2, %s
    mov x0, %s
    mov x1, sp
    mov x8, 64
    svc 1
    """ % (size, out_fd)
    return sc

# read from file descriptor and write to stack


def align4(n):
    m = n % 4
    return n * (m+1)

def generate(in_fd, size):
    """Writes data to stack in thumb mode
    
    Args: 
        in_fd (imm/reg) = file descriptor
        size (int/str)  = 128
    """
    sc = """
    sub sp, #%s
    mov r0, #%s
    mov r2, #%s
    mov r1, sp
    mov r7, #3
    svc 1
    """ % (align4(size), in_fd, size)
    return sc

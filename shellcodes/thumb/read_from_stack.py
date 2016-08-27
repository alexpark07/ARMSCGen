# read from stack and write to file descriptor

def generate(out_fd, size = 'r0'):
    """Writes a file from stack in thumb mode
    
    Args: 
        out_fd (int/str/reg) = file descriptor

        size   (int/str/reg) = size to read
    """

    sc = ""
    try:
        sc += "movs r2, #%s\n" % int(size)
    except:
        sc += "mov r2, %s\n" % size

    try:
        sc += "movs r0, #%s\n" % int(out_fd)
    except:
        sc += "mov r0, %s\n" % out_fd

    sc += """
    mov r1, sp
    movs r7, #4
    svc 1
    """
    return sc

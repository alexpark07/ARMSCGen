# read from stack and write to file descriptor

def generate(out_fd, size):
    """Writes a file from stack in thumb mode
    
    Args: 
        out_fd (int/str/reg) = file descriptor

        size   (int/str/reg) = size to read
    """

    sc = ""
    try:
        sc += "movs r2, #%s\n" % int(out_fd)
    except:
        sc += "mov r2, %s\n" % out_fd

    if size != 'r0':
        try:
            sc += "movs r0, #%s\n" % int(size)
        except:
            sc += "mov r0, %s\n" % size

    sc += """
    mov r1, sp
    movs r7, #4
    svc 1
    """
    return sc

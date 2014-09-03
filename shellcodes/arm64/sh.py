def generate(cmd='/bin/sh'):
    """Executes cmd

    Args:
        cmd(str): executes cmd (default: ``/bin/sh``)
    """
    sc = """
    adr  x0, bin_sh_1
    mov  x2, 0
    str  x0, [sp]
    str  x2, [sp]
    mov  x1, sp
    mov  x8, 221
    svc  0
bin_sh_1:
    .asciz "%s\x00"
    """ % (cmd)
    return sc


def generate(gid=0):
    """setregid(gid, gid) to get egid's privilige
        
        argument:
            gid (int/str/reg) - effective gid number
    """

    if isinstance(gid, int):
        xgid = "#%s" % (gid)
    else:
        xgid = "%s" % (gid)

    sc = """
    mov x0, %s
    mov x1, %s
    mov x8, 143
    svc 1
    """ % (xgid, xgid)
    return sc

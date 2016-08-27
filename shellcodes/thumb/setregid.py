
def generate(gid=0):
    """setregid(gid, gid) to get egid's privilige
        
        argument:
            gid (int/str/reg) - effective gid number
    """
    try:
        xgid = '#%s' % int(gid)
    except:
        xgid = '%s' % gid

    sc = """
    movs r0, %s
    movs r1, %s
    movs r7, #71
    svc 1
    """ % (xgid, xgid)
    return sc

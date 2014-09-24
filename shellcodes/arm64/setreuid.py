
def generate(uid=0):
    """setreuid(uid, uid) to get euid's privilige
    
        Args:
            uid (int/str/reg) - effective uid number
    """

    try:
        xuid = "#%s" % int(uid)
    except:
        xuid = "%s" % (uid)

    sc = """
    mov x0, %s
    mov x1, %s
    mov x8, 145
    svc 1
    """ % (xuid, xuid)
    return sc

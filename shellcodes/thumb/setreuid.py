
def generate(uid=0):
    """setreuid(uid, uid) to get euid's privilige
        
        argument:
            uid (int/str/reg) - effective uid number
    """

    try:
        xuid = "#%s" % int(uid)
    except:
        xuid = "%s" % (uid)

    sc = """
    movs r0, %s
    movs r1, %s
    movs r7, #70
    svc 1
    """ % (xuid, xuid)
    return sc

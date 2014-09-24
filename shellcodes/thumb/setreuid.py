
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
    mov r0, %s
    mov r1, %s
    mov r7, #70
    svc 1
    """ % (xuid, xuid)
    return sc

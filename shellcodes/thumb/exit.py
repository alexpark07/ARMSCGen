# exit(n)

def generate(n=0):
    sc = "\n"
    if n != 0:
        sc += "movs r0, #%s" % int(n)
    else:
        sc += "subs r0, r0, r0"

    sc += """
    movs r7, #1
    svc 1
    """
    return sc

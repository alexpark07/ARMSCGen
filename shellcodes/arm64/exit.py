# exit(n)

def generate(n=0):
    """exit with return code

    Args:
        n(int/str/reg): return code
    """

    sc = "\n"
    try:
        xn = int(n)
        if xn != 0:
            sc += "mov x0, %s" % xn
        else:
            sc += "sub x0, x0, x0"
    except:
        sc += "mov x0, %s" % n

    sc += """
    mov x8, 1
    svc 1
    """
    return sc

if __name__ == '__main__':
    print generate()

# exit(n)

def generate(n=0):
    """exit with return code

    Args:
        n(int/str/reg): return code
    """

    sc = "\n"
    if isinstance(n, int):
        if n != 0:
            sc += "mov x0, %s" % int(n)
        else:
            sc += "sub x0, x0, x0"
    else:
        sc += "mov x0, %s" % n

    sc += """
    mov x8, 1
    svc 1
    """
    return sc

if __name__ == '__main__':
    print generate()

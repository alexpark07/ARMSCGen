# exit(n)

def generate(n=0):
    sc = "\n"
    if n != 0:
        sc += "movw r0, #%s" % int(n)
    else:
        sc += "sub r0, r0, r0"

    sc += """
    mov r7, #1
    svc 0
    """
    return sc

if __name__ == '__main__':
    print generate()

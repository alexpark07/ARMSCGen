def generate(sock=4):
    """Duplicates sock to stdin, stdout and stderr

    Args:
        sock(int/str/reg): sock descriptor

    """
    sc = """
    movs r1, #3
    movs r7, #63
    subs r2, r2, r2
    """
    try:
        xsock = int(sock)
        sc += 'movs r5, #%s' % (xsock)
    except:
        sc += 'movs r5, %s' % (sock)
    sc += """
loop_2:
    movs r0, r5
    subs r1, r1, #1
    svc 1
    cmp r1, r2
    bne loop_2
    """
    return sc

def testcase(sock=4):
    import ARMSCGen as scgen
    scgen.prepareCompiler('THUMB')
    sc = scgen.CompileSC(generate(sock), isThumb=True)
    sclen = len(sc)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

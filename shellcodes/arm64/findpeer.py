# find a peer

def generate():
    """find a socket, which is connected to the specified port
    Leaves socket in x6 regs.

    x6: indicates found socket/file descriptor for backup
    """

    sc = """
findpeer_1:
    sub x5, x5, x5
    add x5, x5, #-1
    mov x3, sp
looplabel_2:
    mov sp, x3
    add x5, x5, #1
    mov x0, x5
    mov x2, #4
    str x2, [sp, 0]
    #push {r2}
    mov x2, sp
    add x1, sp, 32
    mov x8, 205
    svc 1
    cmp x0, #0
    bne looplabel_2
    mov x6, x5
    """
    return sc

if __name__ == '__main__':
    print generate()

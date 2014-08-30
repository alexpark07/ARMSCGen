.global _start
.section .text

_start:
    .arm
    add r6, pc, #1
    bx r6
    .thumb
nanosleep:
    sub r5, r5, r5
    add r5, r5, #1
    sub r6, r6, r6
    push {r5, r6}
    push {r5, r6}
    mov r0, sp
    mov r1, sp
    mov r7, #162
    svc 1
    #svc 0x00900000 + 162

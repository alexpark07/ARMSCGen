.section .text
.global _start

/* /usr/include/asm-generic/unistd.h:#define __NR_execve 221 */
_start:
    adr  x0, bin_sh_1
    mov  x2, 0
    /* push {x0, x2} */
    str  x0, [sp]
    str  x2, [sp]
    mov  x1, sp
    mov  x8, 221
    svc  0

bin_sh_1:
    .asciz "/bin/sh\x00"

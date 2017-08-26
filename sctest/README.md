# emulating shellcodes using unicorn-engine

 * supports for thumb, arm(aarch32) and arm64(aarch64)

## examples

* [thumb-mode dupsh shellcode](sctest/thumb_dupsh.log)
* [arm-mode dupsh shellcode](sctest/arm_dupsh.log)
* [arm64-mode dupsh shellcode](sctest/arm64_dupsh.log)

## usages

```
Usage: sctest.py [options]

ARM32/64 shellcode tester by alex.park

Options:
  -h, --help            show this help message and exit
  -a ARCH, --architechture=ARCH
                        ARM Archtechture (default: arm32 thumb) options:
                        thumb, arm, arm64
  -l LOADFILE, --load-file=LOADFILE
                        shellcode in binary

$ scgen -a thumb dupsh 4 -f r | ./sctest.py

[+] THUMB emulating
[----------------------------------registers-----------------------------------]
  R0 : 0x4L           R1 : 0x2L           R2 : 0x0L           R3 : 0x0L
  R4 : 0x0L           R5 : 0x4L           R6 : 0x0L           R7 : 0x3fL
  R8 : 0x0L           R9 : 0x0L           R10: 0x0L           R11: 0x0L
  IP : 0x0L           SP : 0x2000L        LR : 0x0L           PC : 0x100eL

[-------------------------------------code-------------------------------------]
0x0000100c (0000): 01 df         svc      #1
0x0000100e (0002): 91 42         cmp      r1, r2
0x00001010 (0004): fa d1         bne      #4294967292
0x00001012 (0006): 78 46         mov      r0, pc
0x00001014 (0008): 0b 30         adds     r0, #0xb
0x00001016 (0010): 40 1c         adds     r0, r0, #1
[-----------------------------------syscall------------------------------------]
syscall: dup2
     R0: 0x4L
     R1: 0x2L
     R2: 0x0L
[------------------------------------------------------------------------------]
[----------------------------------registers-----------------------------------]
  R0 : 0x4L           R1 : 0x1L           R2 : 0x0L           R3 : 0x0L
  R4 : 0x0L           R5 : 0x4L           R6 : 0x0L           R7 : 0x3fL
  R8 : 0x0L           R9 : 0x0L           R10: 0x0L           R11: 0x0L
  IP : 0x0L           SP : 0x2000L        LR : 0x0L           PC : 0x100eL

[-------------------------------------code-------------------------------------]
0x0000100c (0000): 01 df         svc      #1
0x0000100e (0002): 91 42         cmp      r1, r2
0x00001010 (0004): fa d1         bne      #4294967292
0x00001012 (0006): 78 46         mov      r0, pc
0x00001014 (0008): 0b 30         adds     r0, #0xb
0x00001016 (0010): 40 1c         adds     r0, r0, #1
[-----------------------------------syscall------------------------------------]
syscall: dup2
     R0: 0x4L
     R1: 0x1L
     R2: 0x0L
[------------------------------------------------------------------------------]
[----------------------------------registers-----------------------------------]
  R0 : 0x4L           R1 : 0x0L           R2 : 0x0L           R3 : 0x0L
  R4 : 0x0L           R5 : 0x4L           R6 : 0x0L           R7 : 0x3fL
  R8 : 0x0L           R9 : 0x0L           R10: 0x0L           R11: 0x0L
  IP : 0x0L           SP : 0x2000L        LR : 0x0L           PC : 0x100eL

[-------------------------------------code-------------------------------------]
0x0000100c (0000): 01 df         svc      #1
0x0000100e (0002): 91 42         cmp      r1, r2
0x00001010 (0004): fa d1         bne      #4294967292
0x00001012 (0006): 78 46         mov      r0, pc
0x00001014 (0008): 0b 30         adds     r0, #0xb
0x00001016 (0010): 40 1c         adds     r0, r0, #1
[-----------------------------------syscall------------------------------------]
syscall: dup2
     R0: 0x4L
     R1: 0x0L
     R2: 0x0L
[------------------------------------------------------------------------------]
[----------------------------------registers-----------------------------------]
  R0 : 0x1022L        R1 : 0x1ff8L        R2 : 0x0L           R3 : 0x0L
  R4 : 0x0L           R5 : 0x4L           R6 : 0x0L           R7 : 0xbL
  R8 : 0x0L           R9 : 0x0L           R10: 0x0L           R11: 0x0L
  IP : 0x0L           SP : 0x1ff8L        LR : 0x0L           PC : 0x1022L

[-------------------------------------code-------------------------------------]
0x00001020 (0000): 01 df         svc      #1
0x00001022 (0002): 2f 62         str      r7, [r5, #0x20]
0x00001024 (0004): 69 6e         ldr      r1, [r5, #0x64]
0x00001026 (0006): 2f 73         strb     r7, [r5, #0xc]
0x00001028 (0008): 68 00         lsls     r0, r5, #1
0x0000102a (0010): 00 00         movs     r0, r0
[-----------------------------------syscall------------------------------------]
syscall: execve
     R0: 2f 62 69 6e 2f 73 68 00 00 00 00 00 00 00 00 00  /bin/sh.........
     R1: 22 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00  "...............
     R2: 0x0L
[------------------------------------------------------------------------------]
[+] done
```

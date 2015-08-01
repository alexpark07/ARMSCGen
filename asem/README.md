# {Dis}Assemble codes in x86/x86_64/arm/thumb(armv7) and arm64

## examples


### i386

```
alex@vm64:~$ shellcraft i386.linux.dupsh 4 -f r | asem -d
0x00000000 (0000): 6a 04                 push     4
0x00000002 (0002): 5b                    pop      ebx
0x00000003 (0003): 6a 03                 push     3
0x00000005 (0005): 59                    pop      ecx
0x00000006 (0006): 49                    dec      ecx
0x00000007 (0007): 6a 3f                 push     0x3f
0x00000009 (0009): 58                    pop      eax
0x0000000a (0010): cd 80                 int      0x80
0x0000000c (0012): 75 f8                 jne      6
0x0000000e (0014): 6a 68                 push     0x68
0x00000010 (0016): 68 2f 2f 2f 73        push     0x732f2f2f
0x00000015 (0021): 68 2f 62 69 6e        push     0x6e69622f
0x0000001a (0026): 89 e3                 mov      ebx, esp
0x0000001c (0028): 31 c9                 xor      ecx, ecx
0x0000001e (0030): 6a 0b                 push     0xb
0x00000020 (0032): 58                    pop      eax
0x00000021 (0033): 99                    cdq      
0x00000022 (0034): cd 80                 int      0x80

alex@vm64:~$ echo "push \$0x732f2f2f" | asem 
"\x68\x2f\x2f\x2f\x73"
```

### amd64 (x64_86)

```
alex@vm64:~$ shellcraft amd64.linux.dupsh 4 -f r | asem -d -a amd64
0x00000000 (0000): 6a 04                           push     4
0x00000002 (0002): 5d                              pop      rbp
0x00000003 (0003): 6a 03                           push     3
0x00000005 (0005): 5e                              pop      rsi
0x00000006 (0006): 48 ff ce                        dec      rsi
0x00000009 (0009): 78 0b                           js       0x16
0x0000000b (0011): 56                              push     rsi
0x0000000c (0012): 48 89 ef                        mov      rdi, rbp
0x0000000f (0015): 6a 21                           push     0x21
0x00000011 (0017): 58                              pop      rax
0x00000012 (0018): 0f 05                           syscall  
0x00000014 (0020): eb ef                           jmp      5
0x00000016 (0022): 6a 68                           push     0x68
0x00000018 (0024): 48 b8 2f 62 69 6e 2f 2f 2f 73   movabs   rax, 0x732f2f2f6e69622f
0x00000022 (0034): 50                              push     rax
0x00000023 (0035): 48 89 e7                        mov      rdi, rsp
0x00000026 (0038): 31 f6                           xor      esi, esi
0x00000028 (0040): 6a 3b                           push     0x3b
0x0000002a (0042): 58                              pop      rax
0x0000002b (0043): 99                              cdq      
0x0000002c (0044): 0f 05                           syscall

alex@vm64:~$ echo "call *%rax;leave;ret" | asem -a amd64
"\xff\xd0\xc9\xc3"
```

### arm32 (aarch32)
```
alex@vm64:~$ scgen -a arm dupsh 4 -f r | asem -d -a arm
0x00000000 (0000): 04 90 a0 e3   mov      sb, #4
0x00000004 (0004): 02 80 a0 e3   mov      r8, #2
0x00000008 (0008): 09 00 a0 e1   mov      r0, sb
0x0000000c (0012): 08 10 a0 e1   mov      r1, r8
0x00000010 (0016): 3f 70 00 e3   movw     r7, #0x3f
0x00000014 (0020): 00 00 00 ef   svc      #0
0x00000018 (0024): 01 80 58 e2   subs     r8, r8, #1
0x0000001c (0028): f9 ff ff 5a   bpl      #8
0x00000020 (0032): 10 00 8f e2   add      r0, pc, #0x10
0x00000024 (0036): 00 20 a0 e3   mov      r2, #0
0x00000028 (0040): 05 00 2d e9   push     {r0, r2}
0x0000002c (0044): 0d 10 a0 e1   mov      r1, sp
0x00000030 (0048): 0b 70 00 e3   movw     r7, #0xb
0x00000034 (0052): 00 00 00 ef   svc      #0
0x00000038 (0056): 2f 62 69 6e   cdpvs    p2, #6, c6, c9, c15, #1
0x0000003c (0060): 2f 73 68 00   rsbeq    r7, r8, pc, lsr #6

alex@vm64:~$ echo "blx r3; pop {r3}; pop {pc}" | asem -a arm
"\x33\xff\x2f\xe1\x04\x30\x9d\xe4\x04\xf0\x9d\xe4"
```

### thumb mode (aarch32-thumb)
```
alex@vm64:~$ scgen -a thumb dupsh 4 -f r | asem -d -a thumb
0x00000000 (0000): 03 21         movs     r1, #3
0x00000002 (0002): 3f 27         movs     r7, #0x3f
0x00000004 (0004): 92 1a         subs     r2, r2, r2
0x00000006 (0006): 04 25         movs     r5, #4
0x00000008 (0008): 28 1c         adds     r0, r5, #0
0x0000000a (0010): 01 39         subs     r1, #1
0x0000000c (0012): 01 df         svc      #1
0x0000000e (0014): 91 42         cmp      r1, r2
0x00000010 (0016): fa d1         bne      #8
0x00000012 (0018): 78 46         mov      r0, pc
0x00000014 (0020): 0a 30         adds     r0, #0xa
0x00000016 (0022): 00 22         movs     r2, #0
0x00000018 (0024): 0b 27         movs     r7, #0xb
0x0000001a (0026): 05 b4         push     {r0, r2}
0x0000001c (0028): 69 46         mov      r1, sp
0x0000001e (0030): 01 df         svc      #1
0x00000020 (0032): 2f 62         str      r7, [r5, #0x20]
0x00000022 (0034): 69 6e         ldr      r1, [r5, #0x64]
0x00000024 (0036): 2f 73         strb     r7, [r5, #0xc]
0x00000026 (0038): 68 00         lsls     r0, r5, #1
0x00000028 (0040): 00 00         movs     r0, r0

alex@vm64:~$ echo "blx r3; pop {r3}; pop {pc}" | asem -a thumb -f h
984708bc00bd
```

### arm64 (aarch64)
```
0x00000000 (0000): 94 00 80 d2   movz     x20, #0x4
0x00000004 (0004): 55 00 80 d2   movz     x21, #0x2
0x00000008 (0008): e0 03 14 aa   mov      x0, x20
0x0000000c (0012): e1 03 15 aa   mov      x1, x21
0x00000010 (0016): 42 00 02 cb   sub      x2, x2, x2
0x00000014 (0020): 08 03 80 d2   movz     x8, #0x18
0x00000018 (0024): 01 00 00 d4   svc      #0
0x0000001c (0028): b5 06 00 d1   sub      x21, x21, #1
0x00000020 (0032): bf 06 00 b1   cmn      x21, #1
0x00000024 (0036): 21 ff ff 54   b.ne     #8
0x00000028 (0040): e0 00 00 10   adr      x0, #0x44
0x0000002c (0044): 02 00 80 d2   movz     x2, #0
0x00000030 (0048): e0 03 00 f9   str      x0, [sp]
0x00000034 (0052): e2 07 00 f9   str      x2, [sp, #8]
0x00000038 (0056): e1 03 00 91   mov      x1, sp
0x0000003c (0060): a8 1b 80 d2   movz     x8, #0xdd
0x00000040 (0064): 01 00 00 d4   svc      #0
0x00000044 (0068): 2f 62 69 6e   rsubhn2  v15.8h, v17.4s, v9.4s

alex@vm64:~$ echo "movz     x2, #0" | asem -a arm64 -f h
020080d2
```

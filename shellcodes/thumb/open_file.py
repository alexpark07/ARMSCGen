import ARMSCGen

O_RDONLY = 00000000
O_WRONLY = 00000001
O_RDWR   = 00000002
O_CREAT  = 00000100
O_APPEND = 00002000

def generate(filepath='./secret', version=3, flags=00, mode=None): 
    """open a file for reading/writing/sending to you in thumb mode

    Args:
        filepath(str): filename to read with flags/mode

        version(int): 2 is old linux kernel including 2.x (default: 3)

        flags(int/str): The argument flags must include one of the following access modes:
                        ``O_RDONLY``, ``O_WRONLY``, or ``O_RDWR``
                        These request opening the file read-only, write-only, or read/write, respectively.

        mode(int/str): modes 

    backup:
        ``r6``: opened file descriptor
    """

    if mode != None:
        sc = ARMSCGen.thumb_fixup('r2', int(mode))
    else:
        sc = ''

    if flags == 0:
        sc += "subs r1, r1, r1\n"
    else:
        sc += ARMSCGen.thumb_fixup('r1', int(flags))

    sc += "mov r0, pc\n"
    sc += "adds r0, #8\n"
    sc += """
    movs r7, #5
    svc 1
    mov r6, r0
    b   after_open_2
filename_1:
    .asciz "%s"
    .align 2
after_open_2:
    """ % (filepath)
    return sc

def testcase(filepath='./secret', version=3, flags=00, mode=None):
    import ARMSCGen as scgen
    sc = scgen.ks_asm('thumb', generate(filepath, flags, mode))[0]
    sclen = len(sc)
    print "[+] Registers information"
    scgen.UC_TESTSC(sc, sclen, scgen.UC_ARCH_ARM, scgen.UC_MODE_THUMB, False)

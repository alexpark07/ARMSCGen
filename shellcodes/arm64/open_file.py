import ARMSCGen

O_RDONLY = 00000000
O_WRONLY = 00000001
O_RDWR   = 00000002
O_CREAT  = 00000100
O_APPEND = 00002000

# openat
AT_FDCWD = -100

def generate(filepath='./secret', flags=00, mode=None): 
    """open a file for reading/writing/sending to you

    Args:
        filepath(str): filename to read with flags/mode
        flags(int/str): The argument flags must include one of the following access modes: ``O_RDONLY``, ``O_WRONLY``, or ``O_RDWR``  
                        These request opening the file read-only, write-only, or read/write, respectively.
        mode(int/str): modes 

    backup:
        ``x6``: opened file descriptor
    """

    if mode != None:
        #sc = ARMSCGen.thumb_fixup('r2', int(mode))
        sc = "mov x3, %s" % (int(mode))
    else:
        sc = ''

    if flags == 0:
        sc += "sub x2, x2, x2"
    else:
        #sc = ARMSCGen.thumb_fixup('r1', int(flags))
        sc = "mov x2, %s" % (int(mode))

    sc += """
    #mov x1, pc
    #add x1, #10
    adr x1, filename_1
    mov x0, %s
    mov x8, 56
    svc 1
    mov x6, x0
    bl after_open_2
filename_1:
    .asciz "%s\x00"
    .align 2
after_open_2:
    """ % (AT_FDCWD, filepath)
    return sc

if __name__ == '__main__':
    print generate(filepath='./binary', flags=O_WRONLY|O_CREAT, mode=0755)

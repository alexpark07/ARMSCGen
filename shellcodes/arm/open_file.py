import ARMSCGen

O_RDONLY = 00000000
O_WRONLY = 00000001
O_RDWR   = 00000002
O_CREAT  = 00000100
O_APPEND = 00002000

def generate(filepath='./secret', flags=00, mode=None): 
    """open a file for reading/writing/sending to you

    Args:
        filepath(str): filename to read with flags/mode

        flags(int/str): The argument flags must include one of the following access modes:
                        ``O_RDONLY``, ``O_WRONLY``, or ``O_RDWR``
                        These request opening the file read-only, write-only, or read/write, respectively.

        mode(int/str): modes 

    backup:
        ``r6``: opened file descriptor
    """

    if mode != None:
        sc = 'movw r2, #%s\n' % (int(mode))
    else:
        sc = ''

    if flags == 0:
        sc += 'sub r1, r1, r1\n'
    else:
        sc += 'movw r1, #%s\n' % (int(flags))

    sc += """
    adr r0, filename_1
    mov r7, #5
    svc 0
    mov r6, r0
    b after_open_2
filename_1:
    .asciz "%s"
    .align 2
after_open_2:
    """ % (filepath)
    return sc

if __name__ == '__main__':
    print generate(filepath='./binary', flags=O_WRONLY|O_CREAT, mode=0755)

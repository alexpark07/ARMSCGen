# open a file
def generate(filepath='./secret', flags=00, mode=None): 
    """open a file for reading/writing/sending to you in thumb mode

    Args:
        filepath (str) : filename to read with flags/mode
        flags (int/str): The argument flags must include one of the following access modes: O_RDONLY, O_WRONLY, or O_RDWR.  
                         These request opening  the  file  read-only,  write-only,  or read/write, respectively.
        mode (int/str) : modes 

    backup:
        r6: opened file's description
    """
    if mode != None:
        sc = 'mov r2, #%s' % (int(mode))
    else:
        sc = ''

    sc += """
    mov r0, pc
    add r0, #12
    mov r1, #0
    mov r7, #(0+ 5)
    svc 1
    mov r6, r0
    bl after_open_2
filename_1:
    .asciz "%s\x00"
    .align 2
after_open_2:
    """ % (filepath)
    return sc

if __name__ == '__main__':
    print generate()

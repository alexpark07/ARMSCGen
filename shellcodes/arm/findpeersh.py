# find a peer with sh

import findpeer
import dupsh

def generate():
    """find a socket, which is connected to the specified port
    Leaves socket in r6 reg.
    """
    sc = findpeer.generate()
    sc += dupsh.generate(sock='r6')
    return sc

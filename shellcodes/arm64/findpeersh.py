import findpeer
import dupsh

def generate():
    """find a socket, which is connected to the specified port
    Leaves socket in x6 reg.
    """

    sc = findpeer.generate()
    sc += dupsh.generate(sock='x6')
    return sc

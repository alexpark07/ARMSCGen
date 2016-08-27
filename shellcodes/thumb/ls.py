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
        r6 reg indicates to file descriptor
    """
    
    sc = ""

    sc += open_file.generate(filepath)
    sc += "subs r4, r4, r4\n"
    sc += "loop_1:\n"
    sc += getdents.generate(in_fd='r6') + '\n'
    sc += """
    cmp r0, r4
    ble after_1
    """
    sc += read_from_stack.generate(int(out_fd)) + '\n'
    sc += """
    cmp r0, r4
    bgt loop_1
after_1:
    """
    return sc

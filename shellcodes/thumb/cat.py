
import open_file
import sendfile

def generate(filepath, in_fd, out_fd):
    """cat a file like UNIX Command

    Args: 
        filepath (str)  : target file name
        in_fd  (int/str): in  file descriptor (default: 'r6' indicates a file descriptor)
        out_fd (int/str): out file descriptor
    """
    sc  = open_file.generate(filepath)
    if in_fd != None:
        sc += sendfile.generate(in_fd, out_fd)
    else:
        sc += sendfile.generate('r6', out_fd)
    return sc

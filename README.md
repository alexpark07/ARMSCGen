### Shellcodes for ARM/Thumb mode

Ideas came from [shell-storm](http://www.shell-storm.org) and [pwntools/pwnies](https://github.com/Gallopsled/pwntools).

Thanks to share all of brilliant sources on the net.

I'm interested in mobile platform and archtecture like Android on ARM, Router on MIPS and so on.

This project named ARMSCGen focus on shellcode on ARM Architecture especially ARMv7 Thumb Mode.

### Requirement

Cross Compile Tool for ARM

``as``, ``ld`` and ``objcopy``

[Capstone](http://www.capstone-engine.org) is needed to disassemble codes.
Install Capstone with:

    $sudo pip install capstone
    
[Unicorn Engine](http://www.unicorn-engine.org/) is needed to emulate shellcodes.
For installing Unicorn Engine, refers to [here](http://www.unicorn-engine.org/docs/)

### Installation

``python setup.py install``

### Usage

reads ``examples`` directory

and

uses ``scgen.py`` in CLI mode

### List of Shellcodes 

please refer to ``shellcodes_lists.md`` or ``scgen -l -a all``

### Documentation

URL: ``http://armscgen.readthedocs.org/`` or ``/docs/`` in source

### TODO

writes shellcodes precisely and writes docs in detail

(To be continued)

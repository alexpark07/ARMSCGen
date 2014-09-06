### Shellcodes for ARM/Thumb mode

Ideas came from [shell-storm](http://www.shell-storm.org) and [pwntools/pwnies](https://github.com/Gallopsled/pwntools).

Thanks to share all of brilliant sources on the net.

I'm interested in mobile platform and archtecture like Android on ARM, Router on MIPS and so on.

This project named ARMSCGen focus on shellcode on ARM Architecture especially ARMv7 Thumb Mode.

### Requirement

1. Cross Compile Tool for ARM

``as``, ``ld`` and ``objcopy``

2. capstone to disassemble codes

URL: http://www.capstone-engine.org/

### Installation

``python setup.py install``

### Usage

reads ``examples`` directory

### Documentation

URL: http://armscgen.readthedocs.org/ or /docs/ in source

### TODO

``AArch64`` shellcodes - writing some shellcodes day by day

``AArch32-ARM Mode`` shellcodes

``Shellcode Generator in CLI mode``

(To be continued)

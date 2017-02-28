### Shellcodes for ARM/Thumb mode

Ideas came from [shell-storm](http://www.shell-storm.org) and [pwntools/pwnies](https://github.com/Gallopsled/pwntools).

Thanks to share all of brilliant sources on the net.

I'm interested in mobile platform and archtecture like Android on ARM, Router on MIPS and so on.

This project named ARMSCGen focus on shellcode on ARM Architecture especially ARMv7 Thumb Mode.

### Requirement

ARMSCGen highly depends on ``{capstone|keystone|unicorn}-engine.``

[Capstone](http://www.capstone-engine.org) is needed to disassemble codes.
Install Capstone with:

``$sudo pip install capstone``

[Keystone](http://www.keystone-engine.org) is needed to assemeble shellcodes.
Install Keystone with:

``$sudo pip install keystone-engine``

or refers to [here](http://www.keystone-engine.org/docs/)
    
[Unicorn Engine](http://www.unicorn-engine.org/) is needed to emulate shellcodes.
For installing Unicorn Engine, refers to [here](http://www.unicorn-engine.org/docs/)

### Installation

``$sudo python setup.py install``

### Usage

reads ``examples`` directory

and

uses ``scgen.py`` in CLI mode

### List of Shellcodes 

please refer to ``shellcodes_lists.md`` or ``scgen -l -a all``

### Notes

Some of thumb mode shellcodes have new option named ``version``.

If you'd like to test shellcodes on old kernel like 2.x then

try to use this option.  ``for example``


```
# linux kernel 2.4 - socketcall
$ scgen -a thumb bindshell 31337 4 2 0 -f a

/* socketcall( socket, { 2, 1, 6 } ) */
movs r1, #2
movs r2, #1
movs r3, #6
push {r1-r3}
movs r0, #1
mov  r1, sp
movs r7, #102
svc 1

# linux kernel 3.x or later
$ scgen -a thumb bindshell 31337 4 3 0 -f a

/* socket(...) */
movs r0, #2
movs r1, #1
subs r2, r2, r2
subs r7, r7, r7
adds r7, r7, #255
adds r7, r7, #26
svc 1 

```

### Documentation

(need to upgrade) URL: ``http://armscgen.readthedocs.org/`` or ``/docs/`` in source

### TODO

writes shellcodes precisely and writes docs in detail

(To be continued)

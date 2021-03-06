syscall_table = {}
syscall_table[202]="accept"
syscall_table[242]="accept4"
syscall_table[1033]="access"
syscall_table[89]="acct"
syscall_table[217]="add_key"
syscall_table[171]="adjtimex"
syscall_table[1059]="alarm"
syscall_table[1075]="bdflush"
syscall_table[200]="bind"
syscall_table[214]="brk"
syscall_table[90]="capget"
syscall_table[91]="capset"
syscall_table[49]="chdir"
syscall_table[1028]="chmod"
syscall_table[1029]="chown"
syscall_table[51]="chroot"
syscall_table[114]="clock_getres"
syscall_table[113]="clock_gettime"
syscall_table[115]="clock_nanosleep"
syscall_table[112]="clock_settime"
syscall_table[220]="clone"
syscall_table[57]="close"
syscall_table[203]="connect"
syscall_table[1064]="creat"
syscall_table[106]="delete_module"
syscall_table[23]="dup"
syscall_table[1041]="dup2"
syscall_table[24]="dup3"
syscall_table[1042]="epoll_create"
syscall_table[20]="epoll_create1"
syscall_table[21]="epoll_ctl"
syscall_table[22]="epoll_pwait"
syscall_table[1069]="epoll_wait"
syscall_table[1044]="eventfd"
syscall_table[19]="eventfd2"
syscall_table[221]="execve"
syscall_table[93]="exit"
syscall_table[94]="exit_group"
syscall_table[48]="faccessat"
syscall_table[223]="fadvise64"
syscall_table[47]="fallocate"
syscall_table[262]="fanotify_init"
syscall_table[263]="fanotify_mark"
syscall_table[50]="fchdir"
syscall_table[52]="fchmod"
syscall_table[53]="fchmodat"
syscall_table[55]="fchown"
syscall_table[54]="fchownat"
syscall_table[25]="fcntl"
syscall_table[1052]="fcntl64"
syscall_table[83]="fdatasync"
syscall_table[10]="fgetxattr"
syscall_table[13]="flistxattr"
syscall_table[32]="flock"
syscall_table[1079]="fork"
syscall_table[16]="fremovexattr"
syscall_table[7]="fsetxattr"
syscall_table[80]="fstat"
syscall_table[1051]="fstat64"
syscall_table[79]="fstatat64"
syscall_table[44]="fstatfs"
syscall_table[1055]="fstatfs64"
syscall_table[82]="fsync"
syscall_table[46]="ftruncate"
syscall_table[1047]="ftruncate64"
syscall_table[98]="futex"
syscall_table[1066]="futimesat"
syscall_table[168]="getcpu"
syscall_table[17]="getcwd"
syscall_table[1065]="getdents"
syscall_table[61]="getdents64"
syscall_table[177]="getegid"
syscall_table[175]="geteuid"
syscall_table[176]="getgid"
syscall_table[158]="getgroups"
syscall_table[102]="getitimer"
syscall_table[236]="get_mempolicy"
syscall_table[205]="getpeername"
syscall_table[155]="getpgid"
syscall_table[1060]="getpgrp"
syscall_table[172]="getpid"
syscall_table[173]="getppid"
syscall_table[141]="getpriority"
syscall_table[150]="getresgid"
syscall_table[148]="getresuid"
syscall_table[163]="getrlimit"
syscall_table[100]="get_robust_list"
syscall_table[165]="getrusage"
syscall_table[156]="getsid"
syscall_table[204]="getsockname"
syscall_table[209]="getsockopt"
syscall_table[178]="gettid"
syscall_table[169]="gettimeofday"
syscall_table[174]="getuid"
syscall_table[8]="getxattr"
syscall_table[105]="init_module"
syscall_table[27]="inotify_add_watch"
syscall_table[1043]="inotify_init"
syscall_table[26]="inotify_init1"
syscall_table[28]="inotify_rm_watch"
syscall_table[3]="io_cancel"
syscall_table[29]="ioctl"
syscall_table[1]="io_destroy"
syscall_table[4]="io_getevents"
syscall_table[31]="ioprio_get"
syscall_table[30]="ioprio_set"
syscall_table[0]="io_setup"
syscall_table[2]="io_submit"
syscall_table[104]="kexec_load"
syscall_table[219]="keyctl"
syscall_table[129]="kill"
syscall_table[1032]="lchown"
syscall_table[9]="lgetxattr"
syscall_table[1025]="link"
syscall_table[37]="linkat"
syscall_table[201]="listen"
syscall_table[11]="listxattr"
syscall_table[12]="llistxattr"
syscall_table[18]="lookup_dcookie"
syscall_table[15]="lremovexattr"
syscall_table[62]="lseek"
syscall_table[6]="lsetxattr"
syscall_table[1039]="lstat"
syscall_table[1050]="lstat64"
syscall_table[233]="madvise"
syscall_table[235]="mbind"
syscall_table[238]="migrate_pages"
syscall_table[232]="mincore"
syscall_table[1030]="mkdir"
syscall_table[34]="mkdirat"
syscall_table[1027]="mknod"
syscall_table[33]="mknodat"
syscall_table[228]="mlock"
syscall_table[230]="mlockall"
syscall_table[222]="mmap"
syscall_table[40]="mount"
syscall_table[239]="move_pages"
syscall_table[226]="mprotect"
syscall_table[185]="mq_getsetattr"
syscall_table[184]="mq_notify"
syscall_table[180]="mq_open"
syscall_table[183]="mq_timedreceive"
syscall_table[182]="mq_timedsend"
syscall_table[181]="mq_unlink"
syscall_table[216]="mremap"
syscall_table[187]="msgctl"
syscall_table[186]="msgget"
syscall_table[188]="msgrcv"
syscall_table[189]="msgsnd"
syscall_table[227]="msync"
syscall_table[229]="munlock"
syscall_table[231]="munlockall"
syscall_table[215]="munmap"
syscall_table[101]="nanosleep"
syscall_table[1054]="newfstatat"
syscall_table[42]="nfsservctl"
syscall_table[1024]="open"
syscall_table[56]="openat"
syscall_table[1061]="pause"
syscall_table[241]="perf_event_open"
syscall_table[92]="personality"
syscall_table[1040]="pipe"
syscall_table[59]="pipe2"
syscall_table[41]="pivot_root"
syscall_table[1068]="poll"
syscall_table[73]="ppoll"
syscall_table[167]="prctl"
syscall_table[67]="pread64"
syscall_table[69]="preadv"
syscall_table[261]="prlimit64"
syscall_table[72]="pselect6"
syscall_table[117]="ptrace"
syscall_table[68]="pwrite64"
syscall_table[70]="pwritev"
syscall_table[60]="quotactl"
syscall_table[63]="read"
syscall_table[213]="readahead"
syscall_table[1035]="readlink"
syscall_table[78]="readlinkat"
syscall_table[65]="readv"
syscall_table[142]="reboot"
syscall_table[1073]="recv"
syscall_table[207]="recvfrom"
syscall_table[243]="recvmmsg"
syscall_table[212]="recvmsg"
syscall_table[234]="remap_file_pages"
syscall_table[14]="removexattr"
syscall_table[1034]="rename"
syscall_table[38]="renameat"
syscall_table[218]="request_key"
syscall_table[128]="restart_syscall"
syscall_table[1031]="rmdir"
syscall_table[134]="rt_sigaction"
syscall_table[136]="rt_sigpending"
syscall_table[135]="rt_sigprocmask"
syscall_table[138]="rt_sigqueueinfo"
syscall_table[139]="rt_sigreturn"
syscall_table[133]="rt_sigsuspend"
syscall_table[137]="rt_sigtimedwait"
syscall_table[240]="rt_tgsigqueueinfo"
syscall_table[123]="sched_getaffinity"
syscall_table[121]="sched_getparam"
syscall_table[125]="sched_get_priority_max"
syscall_table[126]="sched_get_priority_min"
syscall_table[120]="sched_getscheduler"
syscall_table[127]="sched_rr_get_interval"
syscall_table[122]="sched_setaffinity"
syscall_table[118]="sched_setparam"
syscall_table[119]="sched_setscheduler"
syscall_table[124]="sched_yield"
syscall_table[1067]="select"
syscall_table[191]="semctl"
syscall_table[190]="semget"
syscall_table[193]="semop"
syscall_table[192]="semtimedop"
syscall_table[1074]="send"
syscall_table[71]="sendfile"
syscall_table[1046]="sendfile64"
syscall_table[211]="sendmsg"
syscall_table[206]="sendto"
syscall_table[162]="setdomainname"
syscall_table[152]="setfsgid"
syscall_table[151]="setfsuid"
syscall_table[144]="setgid"
syscall_table[159]="setgroups"
syscall_table[161]="sethostname"
syscall_table[103]="setitimer"
syscall_table[237]="set_mempolicy"
syscall_table[154]="setpgid"
syscall_table[140]="setpriority"
syscall_table[143]="setregid"
syscall_table[149]="setresgid"
syscall_table[147]="setresuid"
syscall_table[145]="setreuid"
syscall_table[164]="setrlimit"
syscall_table[99]="set_robust_list"
syscall_table[157]="setsid"
syscall_table[208]="setsockopt"
syscall_table[96]="set_tid_address"
syscall_table[170]="settimeofday"
syscall_table[146]="setuid"
syscall_table[5]="setxattr"
syscall_table[196]="shmat"
syscall_table[195]="shmctl"
syscall_table[197]="shmdt"
syscall_table[194]="shmget"
syscall_table[210]="shutdown"
syscall_table[132]="sigaltstack"
syscall_table[1045]="signalfd"
syscall_table[74]="signalfd4"
syscall_table[1999]="sigreturn"
syscall_table[198]="socket"
syscall_table[199]="socketpair"
syscall_table[76]="splice"
syscall_table[1038]="stat"
syscall_table[1049]="stat64"
syscall_table[43]="statfs"
syscall_table[1056]="statfs64"
syscall_table[225]="swapoff"
syscall_table[224]="swapon"
syscall_table[1036]="symlink"
syscall_table[36]="symlinkat"
syscall_table[81]="sync"
syscall_table[84]="sync_file_range2"
syscall_table[1078]="_sysctl"
syscall_table[179]="sysinfo"
syscall_table[116]="syslog"
syscall_table[77]="tee"
syscall_table[131]="tgkill"
syscall_table[1062]="time"
syscall_table[107]="timer_create"
syscall_table[111]="timer_delete"
syscall_table[85]="timerfd_create"
syscall_table[87]="timerfd_gettime"
syscall_table[86]="timerfd_settime"
syscall_table[109]="timer_getoverrun"
syscall_table[108]="timer_gettime"
syscall_table[110]="timer_settime"
syscall_table[153]="times"
syscall_table[130]="tkill"
syscall_table[45]="truncate"
syscall_table[1048]="truncate64"
syscall_table[166]="umask"
syscall_table[1076]="umount"
syscall_table[39]="umount2"
syscall_table[160]="uname"
syscall_table[1026]="unlink"
syscall_table[35]="unlinkat"
syscall_table[97]="unshare"
syscall_table[1077]="uselib"
syscall_table[1070]="ustat"
syscall_table[1063]="utime"
syscall_table[88]="utimensat"
syscall_table[1037]="utimes"
syscall_table[1071]="vfork"
syscall_table[58]="vhangup"
syscall_table[75]="vmsplice"
syscall_table[260]="wait4"
syscall_table[95]="waitid"
syscall_table[64]="write"
syscall_table[66]="writev"

def get(no):
    return syscall_table[no]

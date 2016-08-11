#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/mman.h>
#include <malloc.h>
 
#define BUFSIZE 1024 
 
int vfunc(char *fn)
{
    void (*fun)();
    char *shellcode;
    char szBuf[4096] = { 0x00, };
    char *p = szBuf;
    int f, rv, cnt;
    FILE *fp;

    shellcode = memalign(4096, 4096);
    mprotect(shellcode, 4096, PROT_READ|PROT_WRITE|PROT_EXEC);
    memset(shellcode, 0, 4096);
    memset(szBuf, 0, sizeof(szBuf));

    fp = fopen(fn, "r");
    cnt = 0;
    while ( 1 ) {
        rv = fread(p, 1, 1, fp);
        p++;
        if( !rv ) break;
        cnt++;
    }
    szBuf[cnt] = '\0';
    fclose(fp);

    printf("cnt: %d\n", cnt);
    memcpy(shellcode, szBuf, cnt);
 
    fun = (void (*)()) shellcode;
    fun();   
 
    return 0;
}
 
void main(int argc, char **argv)
{
    if( argc == 2 ) {
        vfunc(argv[1]);
    }

    return;
}

#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h>
#include <string.h> 
#include <sys/mman.h>
#include <malloc.h>
 
#define BUFSIZE 1024 

int runShellcode(char *sc, int size)
{
    void (*fun)();
    char *shellcode;

    shellcode = memalign(4096, 4096);
    mprotect(shellcode, 4096, PROT_READ|PROT_WRITE|PROT_EXEC);
    memset(shellcode, 0, 4096);

    memcpy(shellcode, sc, size);
 
    fun = (void (*)()) shellcode;
    fun();   
 
    return 0;
}
 
int readFile(char *fn)
{
    char szBuf[4096] = { 0x00, };
    char *p = szBuf;
    int f, rv, cnt;
    FILE *fp;

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

    runShellcode(szBuf, cnt);
 
    return 0;
}

int main(int argc, char **argv)
{
    char ch;
    char szBuf[4096] = { 0x00, };
    int cnt = 0;

    if( argc == 1 ) {
        memset(szBuf, 0x00, sizeof(szBuf));
        while(read(STDIN_FILENO, &ch, 1) > 0) {
            szBuf[cnt] = ch;
            cnt++;
            if( cnt > sizeof(szBuf) ) {
                printf("Your shellcode is too big to load\n");
                return -1;
            }
        }
        szBuf[cnt] = '\0';
        runShellcode(szBuf, cnt);
    } else {
        readFile(argv[1]);
    }

    return 0;
}

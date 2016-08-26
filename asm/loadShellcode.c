#include <stdio.h>

char shellcode[1024] = { 0x00, };

void load(char *fn)
{
	FILE *fp;
    int i, cnt = 0;
	fp = fopen(fn, "r");
    fseek(fp, 0L, SEEK_END);
    cnt = ftell(fp);
    rewind(fp);
    for(i=0; i<cnt; i++)  {
	    fread(shellcode[i], 1, 1, fp);
    }
    shellcode[cnt] = '\0';
	fclose(fp);
}

int main(int argc, char **argv){
	if( argc != 1 ) {
		load(argv[1]);
		fprintf(stdout,"Shellcode length: %d\n", strlen(shellcode));
		(*(void(*)()) shellcode)();
	}
    return 0;
}

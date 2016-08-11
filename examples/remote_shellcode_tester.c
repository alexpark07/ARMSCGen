#include <stdio.h> 
#include <stdlib.h> 
#include <errno.h> 
#include <string.h> 
#include <sys/types.h> 
#include <netinet/in.h> 
#include <sys/socket.h> 
#include <sys/wait.h> 
#include <pwd.h>
#include <sys/mman.h>
#include <malloc.h>
 
#define PORT 31337
#define BACKLOG 100 
#define BUFSIZE 1024 
#define USERNAME "username"
#define DEBUG 0
 
struct sockaddr_in my_addr;
struct sockaddr_in their_addr;
int sin_size;
 
int svr_fd, cli_fd;
 
int SetupSocket()
{
    int sockfd;
 
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        exit(1);
    }
 
    my_addr.sin_family = AF_INET;         
    my_addr.sin_port = htons(PORT);    
    my_addr.sin_addr.s_addr = INADDR_ANY;
    bzero(&(my_addr.sin_zero), 8);    
 
    int option=1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(int)); 
 
    if (bind(sockfd, (struct sockaddr *)&my_addr, sizeof(struct sockaddr)) == -1) {
        perror("bind");
        exit(1);
    }
 
    if (listen(sockfd, BACKLOG) == -1) {
        perror("listen");
        exit(1);
    }
 
    return sockfd;
}
 
void drop_priv()
{
    struct passwd *pw;
    int rv = -1;
 
    pw = getpwnam(USERNAME);
    if ( !pw ) {
        fprintf(stderr, "[ERROR] getpwnam() failed\n");
        exit(-1);
    }
 
    if ( DEBUG ) {
        fprintf(stderr, "[Verbose] pw_name: %s\n", pw->pw_name);
        fprintf(stderr, "[Verbose] pw_passwd: %s\n", pw->pw_passwd);
        fprintf(stderr, "[Verbose] pw_uid: %d\n", pw->pw_uid);
        fprintf(stderr, "[Verbose] pw_gid: %d\n", pw->pw_gid);
        fprintf(stderr, "[Verbose] pw_gecos: %s\n", pw->pw_gecos);
        fprintf(stderr, "[Verbose] pw_dir: %s\n", pw->pw_dir);
        fprintf(stderr, "[Verbose] pw_shell: %s\n", pw->pw_shell);
        fprintf(stderr, "getpwnam: %p\n" , getpwnam);
    }
 
    rv = initgroups(USERNAME, pw->pw_gid);
    if ( 0 != rv ) {
        fprintf(stderr, "[ERROR] initgroups() failed\n");
        exit(-1);
    }
 
    rv = setgid(pw->pw_gid);
    if ( 0 != rv ) {
        fprintf(stderr, "[ERROR] setgid() failed\n");
        exit(-1);
    }
    rv = setuid(pw->pw_uid);
    if ( 0 != rv ) {
        fprintf(stderr, "[ERROR] setuid() failed\n");
        exit(-1);
    }
    rv = chdir(pw->pw_dir);
    if ( 0 != rv ) {
        fprintf(stderr, "[ERROR] chdir() failed\n");
        exit(-1);
    }
}
 
int send_data(int fd, char *msg, int p_numofBytes)
{
    int nReadByte = 0;
    int n = 0;
    char *sendMsg = msg;
 
    while ( nReadByte < p_numofBytes ) {
        n = send(fd, (char *)sendMsg+nReadByte, p_numofBytes-nReadByte, 0);
        nReadByte += n;
        if( n < 0 ) {
            return -1;
        }
    }
 
    return nReadByte;
}
 
int send_string(int fd, char *msg)
{
    return send_data(fd, msg, strlen(msg));
}
 
int recv_data(int fd, char *buf, int nReadBytes)
{
    int cnt = 0;
    int rv = -1;
 
    while ( cnt < nReadBytes && rv ) {
        rv = recv(fd, (char *)buf+cnt, 1, 0);
        if (buf[cnt] == '\n') {
            return cnt;
        }
 
        if ( rv < 0 ) {
            return -1;
        }
        ++cnt;
    }
 
    return cnt;
}
 
void socket_flush(int fd)
{
    int nread = -1;
    char c;
    while( (nread = read(fd, &c, 1, 0)) > 0 ) {
        printf("cleaning...: %c\n", c);
        continue;
    }
}
 
int vfunc(int fd)
{
    void (*fun)();
    char *shellcode;
    char szBuf[4096] = { 0x00, };
    int f, rv;
    f = fd;
    shellcode = memalign(4096, 4096);
    mprotect(shellcode, 4096, PROT_READ|PROT_WRITE|PROT_EXEC);
    memset(shellcode, 0, 4096);
    memset(szBuf, 0, sizeof(szBuf));
    rv = recv_data(f, szBuf, sizeof(szBuf));
    if( rv < 0 ) {
        return -1;
    }
    memcpy(shellcode, szBuf, rv);
 
    fun = (void (*)()) shellcode;
    fun();   
 
    return 0;
}
 
void accept_loop(fd)
{
    int pid;
    int status;
 
    while (1) {  
        sin_size = sizeof(struct sockaddr_in);
        if ((cli_fd = accept(fd, (struct sockaddr *)&their_addr, &sin_size)) == -1) {
            perror("accept");
            continue;
        }
 
        printf("Verbose: connected from %s\n", inet_ntoa(their_addr.sin_addr));
 
        pid = fork();
        if (!pid) { 
            close(svr_fd);
            //drop_priv();
            status = vfunc(cli_fd);
            exit(status);
        }
        else{
            close(cli_fd);  
            while(waitpid(-1,NULL,WNOHANG) > 0); 
        }
    }
}
 
void main(void)
{
    svr_fd = SetupSocket();
    accept_loop(svr_fd);
}
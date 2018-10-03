//gcc -static -o catflag catflag.c
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void printflag(){
    FILE *fp = NULL;
    char buff[255];
    fp = fopen("/flag.txt", "r");
    fgets(buff, 255, (FILE*)fp);
    printf("%s\n", buff);
    fclose(fp); 
}

int main(int argc,char **argv)
{
    int ch;
    int flag = 0;
    // if you call system you go into while, because the source of system call :
    // execl("/bin/sh", "sh", "-c", cmdstring, (char *)0);
    while((ch = getopt(argc, argv, "c:")) != -1) {
        flag = 1;
        switch(ch) {
            case 'c':                
                // printf("option c: %s\n", optarg);
                if (!strcmp(optarg,"sh") || !strcmp(optarg,"/bin/sh"))
                {
                    printflag();
                }else{
                    printf("================================================\n\n");
                    printf("Only support this commands: sh, /bin/sh\n");
                    printf("So you must call system(\"sh\") or system(\"/bin/sh\")\n\n");
                    printf("================================================\n\n");
                }
                break;
            case '?': // 输入未定义的选项, 都会将该选项的值变为 ?
            default:
                printf("Undefined parameter\n");
                printf("Because I change /bin/sh,so if you get shell locally, please add issue on github: \nhttps://github.com/giantbranch/pwn_deploy_chroot\n\n");
        }
    }
    // if you use one_gadget,argc will be 1
    if (argc == 1)
    {
        printflag();
    }else if (flag == 0)
    {
        printf("Because I change /bin/sh,so if you use one_gadget or other technique to get shell locally, please add issue on github: \nhttps://github.com/giantbranch/pwn_deploy_chroot\n\n");
    }
    return 0;
}
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
    while((ch = getopt(argc, argv, "c:")) != -1) {
        switch(ch) {
            case 'c':
                flag = 1;
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
                printf("if you use execl, You can only call execl(\"/bin/sh\", \"/bin/sh\", \"-c\", \"/bin/sh\", 0) \n\n");
                break;
            default:
                printf("if you use execl, You can only call execl(\"/bin/sh\", \"/bin/sh\", \"-c\", \"/bin/sh\", 0) \n\n");
        }
    }
    if (flag == 0)
    {
        printf("if you use execl, You can only call execl(\"/bin/sh\", \"/bin/sh\", \"-c\", \"/bin/sh\", 0) \n\n");
    }
    return 0;
}

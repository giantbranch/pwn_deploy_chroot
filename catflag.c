#include <stdio.h>
 
int main()
{
    FILE *fp = NULL;
    char buff[255];
    fp = fopen("/flag.txt", "r");
    fgets(buff, 255, (FILE*)fp);
    printf("%s\n", buff);
    fclose(fp);
}

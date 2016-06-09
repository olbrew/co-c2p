#include <stdio.h>

char* d = "abc";

int main()
{
    {
        int d = 5;
        d = d*21;    
    }
    d = d*21;
    //printf("%s", d);
    return 0;
}
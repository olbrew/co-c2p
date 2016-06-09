#include <stdio.h>

void increment(int* i);
char cChar();
char c;

int main()
{
    char c = cChar();
	const char f = 'f';
    int i = 5;

    increment(&i);
    printf("\n\nMain:%d", i);
    {
        int a[5];
        a[0]=2;
        for (i=0; i<5; i = i+1)
        {
            if (i == 0)
            {
                continue;
            }
            a[i] = a[i-1]*2;
        }
        i = 0;
        while (i<5)
        {
            printf("\n\nLoop%d:%d", i=i+1, a[i]);
        }
    }
    return 0;
}

void increment(int* i)
{
    printf("\n\nBefore increment:%d", *i);
    *i += 1;
    //Internal scope
	if ('a' == 'a')
    {
        int i = 9;
        printf("\n\nOther:%d", i);
    }
}

char cChar()
{
    
    if ((1==(1-1+2)) || 2==4/2)
    {
        c = 'c';
    }
    else 
    {
        c = 'd';
    }
    return c;
}
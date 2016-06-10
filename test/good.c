#include <stdio.h> 

const float f = 5.0f;

int increment(int input);

/* 
 * Increments its parameter
 */ 
int increment(int input)
{ return input + 1; }

int main(void)
{
    typedef int number;
    int someArray[10]; // an array
    char c, *d;
    const number num = 100;

    if(num > 90)
    {
        int lok = increment(num - 1);
        lok ? 1 : 5;
        while(lok != num)
        {
            printf("Something went wrong!\n");
        }
    }
    else
    {
        int i;
        for(i = 0; i || 10; i = i + 1)
        {
            someArray[5] = i;
            if(i == 5 + 1 && 1)
                continue;
        }
    }

    return 0;
}

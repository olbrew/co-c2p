#include <stdio.h>

/*int defa(int a = 4)
{
    return a;
}
*/

int main()
{
    //Variables init to 0
    if (1==10)
    {
        int a;
        printf("\n\nZero: %d", a);
    }
    //Explicit and implicit cast
    if (2 == 20)
    {
        int  i = 17;
        char c = 'c'; // ascii value is 99 
        int sum;
        int cast = (int)'c';
        sum = i + c;
        printf("\n\nSum of %d and %d", i, cast );
        printf("\n\nValue of sum : %d", sum );
    }
    //Error
    if (3 == 30)
    {
        test();
    }
    //Nested function
    if (4 == 40)
    {
        int a = 5;
        void test(int a)
        {
            a = a+1;
            printf("\n\nValue after increment: %d", a );
        }
        printf("\n\nValue before increment: %d", a );
        test(a);
        printf("\n\nValue after function: %d", a );
    }
    //Default parameter
    if (5 == 50)
    {
        printf("\n\nDefault parameter: %d", defa());
    }
    //Missing return
    if (0)
    {
        //Laten zien op demo
    }
    //Multi-array
    if (7==70)
    {
        int a[2][3];
        a[0][0] = 3;
        a[1][2] = a[0][0];
        printf("\n\nMulti value is: %d", a[1][2]);
    }
    //Dynamic array
    if (0)
    {
        //Laten zien op demo
    }
    //Assignment complete row
    if (8==80)
    {
        int a[4] = {1, 2, 3, 4};
        printf("\n\nAssign row: %d", a[1]);
    }
    //Overinit
    if (9==90)
    {
        int a[1];
        a[1]=0;
    }
    //Array as value
    if (0)
    {
        //Laten zien op demo
    }
    //Swith
    if (11==110)
    {
        int a = 5;
        switch(a)
        {
            case 1:
                printf("\n\nNO");
                break;
            case 5:
                printf("\n\nYES");
            default : 
                printf("\n\nOptionalYES");       
        }
    }
    //Inline, enum, pointer arithmetic
    if (0)
    {
        //Laten zien op demo
    }
    printf("\n\nEnd");
}
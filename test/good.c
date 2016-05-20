#include <stdio.h>

float f = 5.0f;

/*
 * Increments its parameter
 */
int increment(int input) { return input + 1; }

int main(void)
{
    // typedef int number;
    int someArray[10]; // an array
    char c, *d;
    // const number num = 100;
    const int num = 100;

    if (num > 90) {
        int lok = increment(num - 1);

        while (lok != num) {
            printf("Something went wrong!\n");
        }
    } else {
        //int i;
        for (int i = 0; i < 10; i = i + 1) {
            someArray[i] = i;
            if (i == 5 + 1)
                continue;
        }
    }

    return 0;
}

#include <stdio.h>

int* test(int* x, int b) {
    return &b;
}

int main(int p)
{
    int w[5] = {1, 2, 3, 4};
    const char z[5] = {'h', 'e', 'l', 'l', 'o'};
    printf(z);
    scanf(w);

    int d = 1;
    int* p = &d;
    test(p, 1);
    
    return 0;
}

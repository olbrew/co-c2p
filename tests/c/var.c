#include <stdio.h>

// test file for local and global variable support

int a = 2;

void func()
{
    int a = 1;
    printf("function a: %u\n", a);
}

int main()
{
    func();
    printf("global a: %u\n", a);
}

#include <stdio.h>

int glob = 42;

void test()
{
	const int yes = 1;
	int ctr = 1;
	if(yes == 1)
		ctr = 2;
	else 
	{
		int arr[3];
	}
	return;
}

/* comment */
// test

int fib(int what)
{
	if(what <= 2)
		return 1;
	else
		return fib(what-1) + fib(what-2);
}

int main()
{
	int i = 0;
	char c = 'q';
	//int *j = &i;
	float f = 0.5;

        test();
	printf("%d\n", fib(15));
	return fib(15);
}

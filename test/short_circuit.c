#include <stdio.h>

int f()
{	
	return 0;
}

int fail()
{	
	printf("FAIL!!!");
}

int main()
{	
	if(f() && fail())
		return 1;
	else
		return 0;
}

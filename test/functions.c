/*
int test(int argc) {
    return 1;
}

void test1() {
    return 1;
}

int test2() {
    return 1.0f;
}

int test3(int missing) {
    return 1;
}

int test4(int i, int wrong, int a) {
    return 1;
}
*/
void test5(int p, int& ref) {
    
}

int main()
{
    /*
    test3(1);
    
    int i = 0;
    bool b = true;
    int c = 1;
    test4(i, false, c);
    */
    int a = 1;
    int* p = &a;
    test5(*p, a);
    
    return 1;
}
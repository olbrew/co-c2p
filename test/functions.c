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
void test5(int* p, int& ref) {
    
}

int* test6(int* p) {
    return p;
}
/*
int* test7(int& p) {
    return p;
}
int* test8(int p) {
    return p;
}
*/
int& test9(int& p) {
    return p;
}
int& test10(int* p) {
    return p;
}
/*
int& test11(int p) {
    return p;
}*/

int main()
{
    /*
    test3(1);
    
    int i = 0;
    bool b = true;
    int c = 1;
    test4(i, false, c);

    int a = 1;
    int* p = &a;
    test5(*p, a);
    */
    
    int a = 1;
    int* p = &a;
    
    test6(p);  // ok
    //test7(a);  // error
    //test8(a);  // error
    test9(a);   // ok
    test10(p);  // ok
    //test11(a);  // error
    
    return 1;
}

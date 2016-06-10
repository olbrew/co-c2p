int factorial(int n) {
    if (n == 1)
        return 1;
    return n * factorial(n-1);
}

int increment(int i) {
    return i+1;
}

int main() {
    for(int i = 4; i > 1; i = i-1) {
        i*i;
        i+i;
        i/i;
    }

    int i = 5;
    while(i > 2) {
        i*i;
        i+i;
        i/i;
        
        i = i-1;
    }

    return factorial(increment(i));
}

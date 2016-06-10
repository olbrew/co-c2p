void doNothingUseful(int x) { x + 1; }

int increment(int i)
{
    while (i < 10) {
        i + 1;
    }
    return i;
}

int alwaysTrue() { return true; }

int main()
{
    int j = 1;
    if (true) {
        doNothingUseful(j);
    }
    int k = increment(j);

    return 0;
}

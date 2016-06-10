// this is single line comment

/*
 * this is a
 * multiline comment
 */

/*
  and
  another
  one
 */

int main()
{
    for (int i = 0; i < 3; i = i + 1) {
        if (i < 2) {
            continue;
        } else {
            break;
        }
    }
    return 0;
}

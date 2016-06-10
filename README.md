# C2P: Compile SmallC -> P-machine code

This is our project for the [compilers course at the University of Antwerp](https://www.uantwerpen.be/popup/opleidingsonderdeel.aspx?catalognr=1001WETCOP&taal=en&aj=2016).
The goal is to build a compiler capable of translating programs written in a subset of C, [Small-C](http://maestros.unitec.edu/~efutch/small-c__english_version_.html) in instructions for the [P machine](http://ansymore.uantwerpen.be/sites/ansymo.ua.ac.be/files/uploads/courses/Compilers/pMachine/index.html), a Pascal VM.
The compiler is written in Python3 with the help of the [ANTLR tool](http://www.antlr.org/).

### Building
Make sure you have `python3` and `pip3` installed.

If you have you you can run the `build` command. Use `build.sh` on UNIX or
`build.bat` on Windows.

This will automatically install the `antlr4 python3` bindings if you don't have
them yet and generate the needed lexers and parsers from our grammar.

### Running

Run the `test` command. Use `test.sh` on UNIX or `test.bat` on Windows.

This runs the compiler against our test files. As you will notice we have both
*good* and *bad* tests. *Good* tests should run cleanly and *bad* tests
purposefully output errors for their *bad* source files.
You can examine the C source files files contents in the `tests` directory to see
which features our compilers our supports or just read the feature list under
here.

### Implemented features

Feature             | Man / Opt | Status
--------------------|-----------|---------------------------------------------------
char type           | Mandatory | Self explanatory
float type          | Mandatory | ""
int type            | Mandatory | ""
pointer type        | Mandatory | ""
stdio import        | Mandatory | Only allowed include, necessary for `printf` or `scanf`
printf function     | Mandatory | Accepts char[] as well as direct strings.
scanf function      | Mandatory | Syntactic support, no code generation yet
if else             | Mandatory | Self explanatory
return              | Mandatory | ""
while               | Mandatory | ""
local, global vars  | Mandatory | Different scopes can have reinits of same var names
single line comments| Mandatory | Self explanatory
functions           | Mandatory | implemented with robust error checking for return and argument type matches
static arrays       | Mandatory | 1D arrays are supported
for                 | Optional  | Self explanatory
const               | Optional  | ""
break               | Optional  | ""
continue            | Optional  | ""
recursion           | Optional  | ""
multi line comments | Optional  | ""

We make use of our visitor (ASTGenerator) to traverse the parse tree in top down approach. Every rule context from our grammar is visited and saved in our AST which makes use of symbol table and call stack that allows us to verify many consistency errors such as type checking. Once the AST is fully constructed, we finally generate the actual p-code by traversing our AST

## Authors
* Eduard Besjentsev
* Olivier Brewaeys

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

Feature             | Mandatory| Status
------------------- | ---------|--------------------------------------------------
char type           | Mandatory| Fully implemented, errors recognized, ST saves it
float type          | Mandatory| ""
int type            | Mandatory| ""
pointer type        | Mandatory| ""
stdio import        | Mandatory| Only allowed include, necessary for `printf` or `scanf`
printf function     | Mandatory| Accepts char[] as well as direct strings.
scanf function      | Mandatory| TODO?
... WIP

TODO: general explanation about ast completely working and code generation
almost completely :P


## Authors
* Eduard Besjentsev
* Olivier Brewaeys

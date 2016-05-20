# C2P: Compile SmallC -> P-machine code

This is our project for the [compilers course at the University of Antwerp](https://www.uantwerpen.be/popup/opleidingsonderdeel.aspx?catalognr=1001WETCOP&taal=en&aj=2016).
We will build a compiler capable of translating programs written in a subset of C, [Small-C](http://maestros.unitec.edu/~efutch/small-c__english_version_.html),
towards instructions for the [P machine](http://ansymore.uantwerpen.be/sites/ansymo.ua.ac.be/files/uploads/courses/Compilers/pMachine/index.html).
The compiler will be written in Python with the help of the [ANTLR tool](http://www.antlr.org/).

## building and running
Make sure you have `python3` and `pip3` installed.

If you have you you can run the `build` command. Use `build.sh` on UNIX or
`build.bat` on Windows.

This will automatically install the antlr4 python3 bindings if you don't have
them yet, generate the parsers with antlr from our grammar and finally run the
test files.

You can examine the `test.c` files contents in the `test` directory.

## features
The grammar is almost fully complete.
You can test out some intentional errors in the `bad.c` files as described above.
You can also test the `good.c` file and see that the parser doesn't give
errors meaning the grammar supports all constructs used in it.

We are still working on code generation but have already done some work as you
can see in `program.py` in the `src/compiler/nodes` directory.

The code for the symbol table should be nearly complete but is not yet used in
our project.

Finally you can also already see a basis for the AST (Abstract Syntax Tree)
generation. We are using a Visitor pattern to visit the tree nodes.
Currently only the start rule is finished though.

## authors
* Eduard Besjentsev
* Olivier Brewaeys

# C2P: Compile SmallC -> P-machine code

This is our project for the [compilers course at the University of Antwerp](https://www.uantwerpen.be/popup/opleidingsonderdeel.aspx?catalognr=1001WETCOP&taal=en&aj=2016).
We will build a compiler capable of translating programs written in a subset of C, [Small-C](http://maestros.unitec.edu/~efutch/small-c__english_version_.html),
towards instructions for the [P machine](http://ansymore.uantwerpen.be/sites/ansymo.ua.ac.be/files/uploads/courses/Compilers/pMachine/index.html).
The compiler will be written in Python with the help of the [ANTLR tool](http://www.antlr.org/).

## building
Make sure you have the python3 runtime installed. If you don't have it yet you
can install it with `pip`:

    pip3 install antlr4-python-runtime

or alternatively download it [here](https://pypi.python.org/pypi/antlr4-python3-runtime/).

After setting this up you can run the `build` command. Use `build.sh` on UNIX or
`build.bat` on Windows.

## running

To run our test files go into the compiler source folder.
You can now run the intentionally bad C files to see the error checking in
action.

    cd src/compiler/
    python3 C2P.py ../../test/bad1.c output.p
    python3 C2P.py ../../test/bad2.c output.p
    python3 C2P.py ../../test/bad3.c output.p

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

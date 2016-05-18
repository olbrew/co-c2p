#! /bin/bash

## Build
# Install antlr python bindings if they're not yet installed
pip3 install antlr4-python3-runtime==4.5.3
printf "\n"

# Build Grammar Lexers and Parsers with antlr4
java -jar lib/antlr-4.5.3-complete.jar -visitor -Dlanguage=Python3 src/grammar/SmallC.g4
printf "\n"
printf "\n"

## tests
printf "Testing \`test/good.c\`, this should work."
python3 src/C2P.py test/good.c output.p
printf "\n"

echo "Testing \`test/bad.c\` files, these should give errors"
python3 src/C2P.py test/bad1.c output.p
printf "\n"
python3 src/C2P.py test/bad2.c output.p
printf "\n"
python3 src/C2P.py test/bad3.c output.p

#! /bin/bash

# Install antlr python bindings if they're not yet installed
pip3 install antlr4-python3-runtime==4.5.3
printf "\n"

# Build Grammar Lexers and Parsers with antlr4
printf "Building \`smallC\` grammar lexers and parsers"
java -jar lib/antlr-4.5.3-complete.jar -visitor -Dlanguage=Python3 c2p/grammar/SmallC.g4

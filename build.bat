:: Build
:: Install antlr python bindings if they're not yet installed
pip3 install antlr4-python3-runtime==4.5.3
ECHO.

:: Build Grammar Lexers and Parsers with antlr4
java -jar lib/antlr-4.5.3-complete.jar -visitor -Dlanguage=Python3 src/grammar/SmallC.g4
ECHO.
ECHO.

:: tests
ECHO "Testing \`test/good.c\`, this should work."
python3 src/C2P.py test/good.c output.p
ECHO.

ECHO "Testing \`test/bad.c\` files, these should give errors"
python3 src/C2P.py test/bad1.c output.p
ECHO.
python3 src/C2P.py test/bad2.c output.p
ECHO.
python3 src/C2P.py test/bad3.c output.p

:: Keep the CLI open so the user can examine the output of this script
PAUSE

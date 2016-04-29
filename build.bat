java -jar lib/antlr-4.5.3-complete.jar -Dlanguage=Python3 src/grammar/SmallC.g4

:: tests
::python3 src/compiler/C2P.py test/easterfiles/good.c output.p

::echo "Testing bad.c files. These should give errors"
::python3 src/compiler/C2P.py test/easterfiles/bad1.c output.p
::python3 src/compiler/C2P.py test/easterfiles/bad2.c output.p
::python3 src/compiler/C2P.py test/easterfiles/bad3.c output.p

pause
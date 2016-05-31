:: Install antlr python bindings if they're not yet installed
pip3 install antlr4-python3-runtime==4.5.3
ECHO.

:: Build Grammar Lexers and Parsers with antlr4
ECHO "Building `smallC` grammar lexers and parsers"
CD src\grammar\
java -jar ../../lib/antlr-4.5.3-complete.jar -visitor -Dlanguage=Python3 SmallC.g4

@echo OFF

:: Install antlr python bindings if they're not yet installed
pip install antlr4-python3-runtime==4.5.3

:: Build Grammar Lexers and Parsers with antlr4
ECHO "Building `smallC` grammar lexers and parsers"
CD c2p\grammar\
java -jar ../../lib/antlr-4.5.3-complete.jar -visitor -Dlanguage=Python3 SmallC.g4

PAUSE

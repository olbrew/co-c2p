import sys
from antlr4 import *
from HelloLexer import HelloLexer
from HelloParser import HelloParser
#from KeyPrinter import KeyPrinter
from AST import AST

def main(argv):
    input = FileStream(argv[1])
    lexer = HelloLexer(input)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)    
    
    tree = parser.smallc_program()
    #printer = KeyPrinter()
    #walker = ParseTreeWalker()
    #walker.walk(printer, tree)

    ast = AST()

if __name__ == '__main__':
    main(sys.argv)

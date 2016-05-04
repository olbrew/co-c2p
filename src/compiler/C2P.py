import sys

# following 3 lines were necessary to import SmallCLexer and SmallCParser
import os
lib_path = os.path.abspath(os.path.join('..', 'grammar'))
sys.path.append(lib_path)

from antlr4 import *
from SmallCLexer import SmallCLexer
from SmallCParser import SmallCParser
from AST import AST
from ASTGenerator import ASTGenerator


def run(argv):
    input = FileStream(argv[1])
    lexer = SmallCLexer(input)
    stream = CommonTokenStream(lexer)
    parser = SmallCParser(stream)
    tree = parser.smallc_program()

    ast_environment = AST()
    program = ASTGenerator(ast_environment, tree).generate()

    # TODO how to write output of other includes to same .p file
    program.generateCode(argv[2])
    
    return program
    

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('ERROR: 2 arguments needed: `input.c` and `output.p`')
    run(sys.argv)

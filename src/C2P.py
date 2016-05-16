import sys
from antlr4 import FileStream, CommonTokenStream
from grammar.SmallCLexer import SmallCLexer
from grammar.SmallCParser import SmallCParser
from compiler.AST import AST
from compiler.ASTGenerator import ASTGenerator


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

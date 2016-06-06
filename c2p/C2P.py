import sys
import os.path
from antlr4 import FileStream, CommonTokenStream
from grammar.SmallCLexer import SmallCLexer
from grammar.SmallCParser import SmallCParser
from compiler.Environment import Environment
from compiler.ASTGenerator import ASTGenerator
from compiler.MyErrorListener import MyErrorListener, C2PException
from util.DrawAST import draw


def run(input_file, output, saveast):
    lexer = SmallCLexer(FileStream(input_file))
    stream = CommonTokenStream(lexer)
    parser = SmallCParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener())
    parsetree = parser.smallc_program()

    environment = Environment()
    ast = ASTGenerator(environment, parsetree).generate()

    if os.path.isfile(output):
        # empty the file so only new code is saved
        open(output, 'w').close()
    ast.generateCode(output)

    if saveast:
        ast.storeASTToDisk()
        draw(ast)

if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            run(sys.argv[1], sys.argv[2], False)
        elif len(sys.argv) == 4 and sys.argv[3] == "-saveast":
            run(sys.argv[1], sys.argv[2], True)
        else:
            raise C2PException("ERROR: minimum 2 arguments needed: `input.c` \
                            and `output.p`, with an optional -saveast as last argument")
    except C2PException as error:
        print(error)

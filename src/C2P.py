import sys
import os.path
from antlr4 import FileStream, CommonTokenStream
from grammar.SmallCLexer import SmallCLexer
from grammar.SmallCParser import SmallCParser
from compiler.AST import AST
from compiler.ASTGenerator import ASTGenerator
from compiler.MyErrorListener import MyErrorListener, C2PException

def run(argv):
    inputfile = FileStream(argv[1])
    outputfile = argv[2]
    lexer = SmallCLexer(inputfile)
    stream = CommonTokenStream(lexer)
    parser = SmallCParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener())
    parsetree = parser.smallc_program()

    environment = AST()
    ast = ASTGenerator(environment, parsetree).generate()
    
    if os.path.isfile(outputfile):
        # empty the file so only new code is saved
        open(outputfile, 'w').close()
    ast.generateCode(outputfile)

    # test (de)serialization of AST
    ast.storeASTToDisk()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('ERROR: 2 arguments needed: `input.c` and `output.p`')
    
    try:
        run(sys.argv)
    except C2PException as error:
        print(error)

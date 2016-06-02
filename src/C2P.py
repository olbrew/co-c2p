import sys
import os.path
from antlr4 import FileStream, CommonTokenStream
from grammar.SmallCLexer import SmallCLexer
from grammar.SmallCParser import SmallCParser
from compiler.AST import AST
from compiler.ASTGenerator import ASTGenerator
from compiler.MyErrorListener import MyErrorListener

def run(argv):
    inputfile = FileStream(argv[1])
    outputfile = argv[2]
    lexer = SmallCLexer(inputfile)
    stream = CommonTokenStream(lexer)
    parser = SmallCParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener())
    try:
        tree = parser.smallc_program()
        ast_environment = AST()
        program = ASTGenerator(ast_environment, tree).generate()
        
        if os.path.isfile(outputfile):
            # empty the file so only new code is saved
            open(outputfile, 'w').close()
        program.generateCode(outputfile)

        # test (de)serialization of AST
        program.storeASTToDisk()    
        ast = program.loadASTFromDisk()
        
        return program
    except Exception as error:
        print(error)
        sys.exit


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('ERROR: 2 arguments needed: `input.c` and `output.p`')
    run(sys.argv)

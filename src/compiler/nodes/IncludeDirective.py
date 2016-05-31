from compiler.ASTNode import ASTNode
from compiler.types.IntegerType import IntegerType

class IncludeDirective(ASTNode):
    # TODO only support include stio, put them directly in symbol table

    def __init__(self, ast, filename):
        super().__init__(ast)
        self.filename = filename
        
        if self.filename == "stdio.h":
            # TODO: determine address for following two symbols
            ast.symbol_table.addSymbol("printf", IntegerType(), "", 0)
            ast.symbol_table.addSymbol("scanf", IntegerType(), "", 0)

    def getDisplayableText(self):
        return "include '" + self.filename + "'"

    def generateCode(self, out):
        # TODO
        '''
        for include in self.included_program.includes:
            include.generateCode(out)

        for func_decl in self.included_program.function_declarations:
            func_decl.generateCode(out)
        '''
        pass

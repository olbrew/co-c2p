from compiler.ASTNode import ASTNode
from compiler.types.IntegerType import IntegerType

class IncludeDirective(ASTNode):

    def __init__(self, ast, filename):
        super().__init__(ast)
        self.filename = filename
        
        if self.filename == "stdio.h":
            address = ast.call_stack.getAddress()
            depth = ast.call_stack.getNestingDepth()
            ast.symbol_table.addSymbol("printf", IntegerType(), address, depth)
            ast.symbol_table.addSymbol("scanf", IntegerType(), address, depth)

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

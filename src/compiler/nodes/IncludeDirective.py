from compiler.ASTNode import ASTNode


class IncludeDirective(ASTNode):
    # TODO only support include stio, put them directly in symbol table

    def __init__(self, ast, filename):
        super().__init__(ast)
        self.filename = filename

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

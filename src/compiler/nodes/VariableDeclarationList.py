from compiler.ASTNode import ASTNode


class VariableDeclarationList(ASTNode):

    def __init__(self, ast):
        super().__init__(ast)

    def getDisplayableText(self):
        return "var decl list"

    def generateCode(self, out):
        # TODO Auto-generated method stub
        pass

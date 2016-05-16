import ASTNode

class VariableDeclarationList(ASTNode):    
    def __init__(self, ast):
        ASTNode.__init__(self, ast)
    
    def getDisplayableText(self):
        return "var decl list"
        
    def generateCode(self, out):
        # TODO Auto-generated method stub
        pass

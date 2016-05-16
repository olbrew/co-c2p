import ASTNode

class ParameterList(ASTNode):
    def __init__(self, ast, arguments):
        ASTNode.__init__(self, ast)
        self.arguments = arguments
        for expression in self.arguments:
            self.addChild(expression)
        
    def getDisplayableText(self):
        return "parameter list"
        
    def generateCode(self, out):
        # TODO Auto-generated method stub
        pass


from AST import AST
from ASTNode import ASTNode

class ParameterDeclarationList(ASTNode):    
    def __init__(self, ast, params, parameter_pack):
        ASTNode.__init__(self, ast)
        
        self.parameters = params
        self.parameter_pack = parameter_pack
        
        for param in self.parameters:
            self.addChild(param)
    
    
    def getDisplayableText(self):
        return "parameter list"
        
        
    def generateCode(self, out):
        return

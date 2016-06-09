from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class VariableDeclarationList(ASTNode):

    def __init__(self, environment, variable_ids):
        super().__init__(environment, SmallCParser.VARIABLEDECLARATIONLIST)
        self.variable_ids = variable_ids
        for var_id in self.variable_ids:
            self.addChild(var_id)
        
    def getDisplayableText(self):
        return "var decl list"
        
    def getDeclarationSize(self):
        space = 0

        for var_id in self.variable_ids:
            space += var_id.getSize()

        return space

    def generateCode(self, out):
        pass
        # variable_ids are already generated via VariableDeclaration

from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class VariableDeclarationList(ASTNode):

    def __init__(self, environment, variable_ids):
        super().__init__(environment, SmallCParser.VARIABLEDECLARATIONLIST)
        self.variable_ids = variable_ids
        
    def getDisplayableText(self):
        return "var decl list"

    def generateCode(self, out):
        # TODO verify this is correct
        for var_id in self.variable_ids:
            self.generateCode(var_id)

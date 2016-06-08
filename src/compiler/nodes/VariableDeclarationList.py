from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class VariableDeclarationList(ASTNode):

    def __init__(self, environment):
        super().__init__(environment, SmallCParser.VARIABLEDECLARATIONLIST)

    def getDisplayableText(self):
        return "var decl list"

    def generateCode(self, out):
        # TODO Auto-generated method stub
        pass

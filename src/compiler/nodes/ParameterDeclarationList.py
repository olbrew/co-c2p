from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class ParameterDeclarationList(ASTNode):

    def __init__(self, ast, params):
        super().__init__(ast, SmallCParser.PARAMETERDECLARATIONLIST)

        self.parameters = params

        for param in self.parameters:
            self.addChild(param)

    def getDisplayableText(self):
        return "parameter list"

    def generateCode(self, out):
        return

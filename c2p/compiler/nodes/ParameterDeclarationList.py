from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class ParameterDeclarationList(ASTNode):

    def __init__(self, environment, params):
        super().__init__(environment, SmallCParser.PARAMETERDECLARATIONLIST)

        self.parameter_list = params

        for param in self.parameter_list:
            self.addChild(param)

    def getDisplayableText(self):
        return "parameter declaration list"

    def generateCode(self, out):
        return

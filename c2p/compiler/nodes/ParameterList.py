from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class ParameterList(ASTNode):

    def __init__(self, environment, arguments):
        super().__init__(environment, SmallCParser.PARAMETERLIST)
        self.arguments = arguments
        for expression in self.arguments:
            self.addChild(expression)

    def getDisplayableText(self):
        return "parameter list"

    def generateCode(self, out):
        for arg in self.arguments:
            arg.generateCode(out)

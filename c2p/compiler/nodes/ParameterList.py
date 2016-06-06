from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class ParameterList(ASTNode):

    def __init__(self, ast, arguments):
        super().__init__(ast, SmallCParser.PARAMETERLIST)
        self.arguments = arguments
        for expression in self.arguments:
            self.addChild(expression)

    def getDisplayableText(self):
        return "parameter list"

    def generateCode(self, out):
        # TODO Auto-generated method stub
        pass

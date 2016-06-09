from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class ParameterDeclarationList(ASTNode):

    def __init__(self, environment, parameter_declarations):
        super().__init__(environment, SmallCParser.PARAMETERDECLARATIONLIST)

        self.parameter_declarations = parameter_declarations

        for param_decl in self.parameter_declarations:
            self.addChild(param_decl)

    def getDisplayableText(self):
        return "parameter declaration list"

    def generateCode(self, out):
        return

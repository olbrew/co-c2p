from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class WriteIntStatement(ASTNode):

    def __init__(self, environment, expression):
        super().__init__(environment, SmallCParser.WRITEINTSTATEMENT)
        self.expression = expression
        self.addChild(expression)

    def getDisplayableText(self):
        return "writeint"

    def generateCode(self, out):
        self.expression.generateCode(out)
        self.writeInstruction("out i", out)
        self.writeInstruction("ldc c '\\n'", out)

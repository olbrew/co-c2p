from compiler.ASTNode import ASTNode


class WriteIntStatement(ASTNode):

    def __init__(self, ast, expression):
        super().__init__(ast)
        self.expression = expression
        self.addChild(expression)

    def getDisplayableText(self):
        return "writeint"

    def generateCode(self, out):
        self.expression.generateCode(out)
        self.writeInstruction("out i", out)
        self.writeInstruction("ldc c '\\n'", out)

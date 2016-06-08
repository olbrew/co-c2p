from .Statement import Statement
from grammar.SmallCParser import SmallCParser


class IfStatement(Statement):
    label_counter = 0

    def __init__(self, environment, expression, if_statement):
        super().__init__(environment)
        self.type = SmallCParser.IFSTATEMENT
        self.expression = expression
        self.if_statement = if_statement
        self.addChild(self.expression)
        self.addChild(self.if_statement)

    def getDisplayableText(self):
        return "if"

    def generateCode(self, out):
        # First get the result of the condition on top of the stack
        self.expression.generateCode(out)

        # Evaluate it
        self.writeInstruction(
            "fjp if_" + str(IfStatement.label_counter) + "_end", out)

        # if the condition is true, execute the statement
        self.if_statement.generateCode(out)
        self.writeInstruction(
            "if_" + str(IfStatement.label_counter) + "_end:", out)

        IfStatement.label_counter += 1

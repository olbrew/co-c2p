from .IfStatement import IfStatement
from grammar.SmallCParser import SmallCParser


class IfElseStatement(IfStatement):

    def __init__(self, ast, expression, if_statement, else_statement):
        super().__init__(ast, expression, if_statement)
        self.type = SmallCParser.IFELSESTATEMENT
        self.else_statement = else_statement
        self.addChild(self.else_statement)

    def getDisplayableText(self):
        return "if else"

    def generateCode(self, out):
        # First get the result of the condition on top of the stack
        self.expression.generateCode(out)

        # Evaluate it
        self.writeInstruction(
            "fjp if_" + str(IfStatement.label_counter) + "_false", out)

        # if the condition is true, execute the statement
        self.if_statement.generateCode(out)
        self.writeInstruction(
            "ujp if_" + str(IfStatement.label_counter) + "_end", out)
        self.writeInstruction(
            "if_" + str(IfStatement.label_counter) + "_false:", out)

        # if the condition is true, execute the alternative statement
        self.else_statement.generateCode(out)
        self.writeInstruction(
            "if_" + str(IfStatement.label_counter) + "_end:", out)

        IfStatement.label_counter += 1

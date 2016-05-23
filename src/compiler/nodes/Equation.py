import sys
from .Expression import Expression


class Equation(Expression):

    def __init__(self, ast, expression_equation, expression_term, operator):
        super().__init__(ast)
        self.equation = expression_equation
        self.term = expression_term
        self.operator = operator
        self.addChild(self.equation)
        self.addChild(self.term)
        self.operand_type = self.equation.result_type.getPoorest(
            self.term.result_type)
        self.result_type = self.operand_type

    def getDisplayableText(self):
        return self.operator

    def generateCode(self, out):
        # Get p-code datatype for this expression
        p_type = self.operand_type.getPSymbol()

        # First get the operands on top of the stack
        self.equation.generateCode(out)
        self.cast(self.equation, out)

        # Execute the relevant operation on the operands
        if self.operator == "+":
            self.writeInstruction("add " + p_type, out)
        elif self.operator == "-":
            self.writeInstruction("sub " + p_type, out)
        else:
            print("Error:", self.operator, " is not implemented.")
            sys.exit(1)

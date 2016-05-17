import sys
from .Expression import Expression
from compiler.types.BooleanType import BooleanType


class Comparison(Expression):

    def __init__(self, ast, expr_relation1, expr_relation2, operator):
        Expression.__init__(self, ast)
        self.relation1 = expr_relation1
        self.relation2 = expr_relation2
        self.operator = operator
        self.addChild(self.relation1)
        self.addChild(self.relation2)
        self.operand_type = self.relation1.result_type.getPoorest(
            self.relation2.result_type)
        self.result_type = BooleanType()

    def getDisplayableText(self):
        return self.operator

    def generateCode(self, out):
        # Get p-code datatype for this expression
        p_type = self.operand_type.getPSymbol()

        # First get the operands on top of the stack
        self.relation1.generateCode(out)
        self.cast(self.relation1, out)
        self.relation2.generateCode(out)
        self.cast(self.relation2, out)

        # Execute the operation on the operands
        if self.operator is "==":
            self.writeInstruction("equ " + p_type, out)
        elif self.operator is "!=":
            self.writeInstruction("neq " + p_type, out)
        else:
            print("Error:", self.operator, " is not implemented.")
            sys.exit(1)

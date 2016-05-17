import sys
from .Expression import Expression


class Term(Expression):

    def __init__(self, ast, expression_term, expression_factor, operator):
        super().__init__(ast)
        self.term = expression_term
        self.factor = expression_factor
        self.operator = operator
        self.addChild(self.term)
        self.addChild(self.factor)
        self.operand_type = self.term.result_type.getPoorest(
            self.factor.result_type)
        self.result_type = self.operand_type

    def getDisplayableText(self):
        return self.operator

    def generateCode(self, out):
        # Get p-code datatype for this expression
        p_type = self.operand_type.getPSymbol()

        # Get the first operand on top of the stack
        self.term.generateCode(out)
        self.cast(self.term, out)

        # Execute the relevant operation on the operands ('*' and '/' load
        # the factor in the condition to permit '%' to execute it later)
        if self.operator is "*":
            self.factor.generateCode(out)
            self.cast(self.factor, out)
            self.writeInstruction("mul " + p_type, out)
        elif self.operator is "/":
            self.factor.generateCode(out)
            self.cast(self.factor, out)
            self.writeInstruction("div " + p_type, out)
        elif self.operator is "%":
            # Duplicate the result of the term first, instead of recomputing it
            # This way we effectively cut the cost of the second computation
            # TODO: try to find a way to duplicate the factor as well, instead of
            # computing it twice
            self.writeInstruction("dpl " + p_type, out)
            self.factor.generateCode(out)
            self.cast(self.factor, out)
            self.writeInstruction("div " + p_type, out)
            self.factor.generateCode(out)
            self.cast(self.factor, out)
            self.writeInstruction("mul " + p_type, out)
            self.writeInstruction("sub " + p_type, out)
        else:
            print("Error:", self.operator, " is not implemented.")
            sys.exit(1)

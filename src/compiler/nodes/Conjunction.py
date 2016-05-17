from compiler.types.BooleanType import BooleanType
from .Expression import Expression


class Conjunction(Expression):

    def __init__(self, ast, expr_conjunction, expr_comparison):
        super().__init__(ast)
        self.conjunction = expr_conjunction
        self.comparison = expr_comparison
        self.addChild(self.conjunction)
        self.addChild(self.comparison)
        self.operand_type = BooleanType()
        self.result_type = BooleanType()

    def getDisplayableText(self):
        return "and"

    def generateCode(self, out):
        # first get the operands on top of the stack
        self.conjunction.generateCode(out)
        self.cast(self.conjunction, out)
        self.comparison.generateCode(out)
        self.cast(self.comparison, out)
        # execute the operation on the operands
        self.writeInstruction("and", out)

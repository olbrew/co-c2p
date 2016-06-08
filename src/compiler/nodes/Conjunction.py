from compiler.types.BooleanType import BooleanType
from .Expression import Expression
from grammar.SmallCParser import SmallCParser


class Conjunction(Expression):

    def __init__(self, environment, expr_conjunction, expr_comparison):
        super().__init__(environment)
        self.type = SmallCParser.CONJUNCTION
        self.conjunction = expr_conjunction
        self.comparison = expr_comparison
        self.addChild(self.conjunction)
        self.addChild(self.comparison)
        self.operand_type = BooleanType()
        self.result_type = BooleanType()

    def getDisplayableText(self):
        return "&&"

    def generateCode(self, out):
        # first get the operands on top of the stack
        self.conjunction.generateCode(out)
        self.cast(self.conjunction, out)
        self.comparison.generateCode(out)
        self.cast(self.comparison, out)
        # execute the operation on the operands
        self.writeInstruction("and", out)

from compiler.types.BooleanType import BooleanType
from .Expression import Expression
from compiler.MyErrorListener import C2PException


class Factor(Expression):

    def __init__(self, ast, factor, operator):
        super().__init__(ast)
        self.factor = factor
        self.operator = operator
        self.addChild(self.factor)

        if self.operator == "!":
            self.operand_type = BooleanType()
        else:
            self.operand_type = self.factor.result_type
        self.result_type = self.operand_type

    def getDisplayableText(self):
        return self.operator

    def generateCode(self, out):
        # first get the operand on top of the stack
        self.factor.generateCode(out)
        self.cast(self.factor, out)

        # execute the relevant operation on the operand
        if self.operator == "-":
            self.writeInstruction("neg " + self.operand_type.getPSymbol(), out)
        elif self.operator == "!":
            self.writeInstruction("not ", out)
        else:
            raise C2PException(self.operator + " is not supported")

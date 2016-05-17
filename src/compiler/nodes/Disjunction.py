from compiler.types.Type import Type
from .Expression import Expression


class Disjunction(Expression):
    
    def __init__(self, ast, expr_disjunction, expr_conjunction):
        super().__init__(self, ast)
        self.disjunction = expr_disjunction
        self.conjunction = expr_conjunction
        self.addChild(self.disjunction)
        self.addChild(self.conjunction)
        self.operand_type = BooleanType()
        self.result_type = BooleanType()
        
    def getDisplayableText(self):
        return "or"
    
    def generateCode(self, out):
        # first get the operands on top of the stack
        self.disjunction.generateCode(out)
        self.cast(self.disjunction, out)
        self.conjunction.generateCode(out)
        self.cast(self.conjunction, out)
        # execute the operation on the operands
        self.writeInstruction("or", out)

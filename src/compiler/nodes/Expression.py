from .Statement import Statement
from grammar.SmallCParser import SmallCParser


class Expression(Statement):

    def __init__(self, ast):
        super().__init__(ast)
        self.type = SmallCParser.EXPRESSION
        self.operand_type = None
        self.result_type = None

    def cast(self, expression, out):
        expr_result_type = expression.result_type
        expr_operand_type = expression.operand_type
        
        if expr_operand_type.getName() != expr_result_type.getName():
            self.writeInstruction("conv " + expr_result_type.getPSymbol() +
                                  " " + expr_operand_type.getPSymbol(), out)
            print("WARNING: implicit cast from '" + expr_operand_type.getName() + "' to '" + expr_result_type.getName() + "'. Information could be lost.")

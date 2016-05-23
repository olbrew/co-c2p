from .Statement import Statement


class Expression(Statement):

    def __init__(self, ast):
        super().__init__(ast)
        self.operand_type = None
        self.result_type = None

    def cast(self, expression, out):
        expr_result_type = expression.result_type
        expr_operand_type = expression.operand_type
        
        if expr_operand_type.getName() != expr_result_type.getName():
            self.writeInstruction("conv " + expr_result_type.getPSymbol() +
                                  " " + expr_operand_type.getPSymbol(), out)
            # TODO: warn that this is an implicit cast and information could be
            # lost

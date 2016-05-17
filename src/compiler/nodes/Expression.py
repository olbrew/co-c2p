from .Statement import Statement


class Expression(Statement):

    def __init__(self, ast):
        super().__init__(ast)

        self.operand_type = None
        self.result_type = None
        # TODO: does result_type or operand_type need to be initialized?

    def cast(self, expression, out):
        expr_type = expression.result_type
        if self.operand_type.getName() != expr_type.getName():
            self.writeInstruction("conv " + expr_type.getPSymbol() +
                                  " " + self.operand_type.getPSymbol(), out)
            # TODO: warn that this is an implicit cast and information could be
            # lost

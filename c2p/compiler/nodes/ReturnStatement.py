from .Statement import Statement
from .Function import Function
from .ControlStructure import ControlStructure
from compiler.types.VoidType import VoidType
from grammar.SmallCParser import SmallCParser


class ReturnStatement(Statement):

    def __init__(self, environment, expression):
        super().__init__(environment)
        self.type = SmallCParser.RETURNSTATEMENT
        self.expression = expression
        self.addChild(self.expression)

    def getDisplayableText(self):
        return "return"

    def generateCode(self, out):
        # Find the owning function
        node = self
        controlStructure = None
        while not isinstance(node, Function):
            node = node.parent
            if (controlStructure is None) and isinstance(node, ControlStructure):
                controlStructure = node
        function = node

        self.expression.generateCode(out)

        expr_type = self.expression.result_type
        return_type = function.return_type
        if not isinstance(expr_type, VoidType):
            # TODO warning for implicit cast
            if expr_type.getName() is not return_type.getName():
                self.writeInstruction(
                    "conv " + expr_type.getPSymbol() + " " + return_type.getPSymbol(), out)
                print("WARNING: implicit cast from '" + expr_type.getName() +
                      "' to '" + return_type.getName() + "'. Information could be lost.")

        self.writeInstruction("str " + return_type.getPSymbol() + str(
            self.environment.call_stack.getNestingDepth() - function.depth) + " 0", out)
        self.writeInstruction("ujp " + controlStructure.getReturnLabel(), out)

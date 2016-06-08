from .Expression import Expression
from compiler.MyErrorListener import C2PException
from grammar.SmallCParser import SmallCParser


class Assignment(Expression):

    def __init__(self, environment, identifier, expression):
        super().__init__(environment)
        self.type = SmallCParser.ASSIGNMENT
        self.identifier = identifier
        self.expression = expression
        self.addChild(self.expression)

        symbol = environment.symbol_table.getSymbol(self.identifier)
        if symbol is None:
            raise C2PException(
                "Can't assign to undeclared variable '" + self.identifier + "'")        
        self.expression.result_type = symbol.type
        self.address = symbol.address
        self.depth = symbol.getRelativeDepth(environment.call_stack)
        self.expression.operand_type = self.expression.result_type

        if self.expression.result_type.is_const:
            raise C2PException(
                "Can't assign to const variable '" + self.identifier + "'")

    def getDisplayableText(self):
        return "="

    def generateCode(self, out):
        self.expression.generateCode(out)
        self.cast(self.expression, out)

        # implicitly cast if necessary
        self.cast(self.expression, out)  # TODO verify whether this is correct

        self.writeInstruction("str " + self.expression.result_type.getPSymbol() + " " +
                              str(self.depth) + " " + str(self.address), out)

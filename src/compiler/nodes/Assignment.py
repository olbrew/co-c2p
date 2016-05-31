#from compiler.types.Type import Type
from .Expression import Expression
#from compiler.AST import AST
#from compiler.SymbolTable import Symbol, SymbolTable


class Assignment(Expression):

    def __init__(self, ast, identifier, expression, array_index):
        super().__init__(ast)
        self.identifier = identifier
        self.expression = expression
        self.addChild(self.expression)
        self.array_index = array_index

        symbol = ast.symbol_table.getSymbol(self.identifier)
        self.expression.result_type = symbol.type
        self.address = symbol.address
        self.depth = symbol.getRelativeDepth(ast.call_stack)
        self.expression.operand_type = self.expression.result_type

        if self.expression.result_type.is_const:
            # TODO: handle this properly with a semantic exception
            raise Exception("Can't assign to const variable '" + self.identifier + "'!")

    def getDisplayableText(self):
        return "assignment"

    def generateCode(self, out):
        self.expression.generateCode(out)
        self.cast(self.expression, out)

        # implicitly cast if necessary
        self.cast(self.expression, out)

        self.writeInstruction("str " + self.expression.result_type.getPSymbol() + " " +
                              str(self.depth) + " " + str(self.address + self.array_index), out)

from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class VariableIdentifier(ASTNode):

    def __init__(self, ast, identifier, expression, is_pointer, array_size):
        super().__init__(ast, SmallCParser.VARIABLEIDENTIFIER)

        self.typename = None
        self.identifier = identifier
        self.expression = expression
        self.is_pointer = is_pointer
        self.array_size = array_size
        self.address = None
        self.depth = None

        if expression is not None:
            self.addChild(expression)

    def allocate(self):
        space = self.getSize()
        self.address = self.ast.call_stack.getAddress(space)
        self.depth = self.ast.call_stack.getNestingDepth()
        self.ast.symbol_table.addSymbol(
            self.identifier, self.typename, self.address, self.depth)

    def setType(self, typename):
        self.typename = typename
        if self.is_pointer:
            self.typename.is_pointer = True

        self.typename.array_size = self.array_size
        self.allocate()

    def getSize(self):
        if self.array_size > 0:
            return self.array_size
        else:
            return 1

    def getDisplayableText(self):
        return "var identifier"

    def generateCode(self, out):
        p_type = "a" if self.is_pointer else self.typename.getPSymbol()

        if self.expression is not None:
            self.expression.generateCode(out)
        else:
            self.writeInstruction("ldc " + p_type + " 0", out)

        self.writeInstruction("str " + p_type + " " +
                              str(0) + " " + str(self.address), out)

        for i in range(1, self.getSize()):
            self.writeInstruction("ldc " + p_type + " 0", out)
            self.writeInstruction("str " + p_type + " " +
                                  str(0) + " " + str(self.address + i), out)

from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser
from compiler.MyErrorListener import C2PException


class VariableIdentifier(ASTNode):

    def __init__(self, environment, identifier, expression, is_pointer, is_alias, array_size):
        super().__init__(environment, SmallCParser.VARIABLEIDENTIFIER)

        self.typename = None
        self.identifier = identifier
        self.expression = expression
        self.is_pointer = is_pointer
        self.is_alias = is_alias
        self.array_size = array_size
        self.address = None
        self.depth = None

        if self.expression is not None:
            self.addChild(self.expression)

    def allocate(self):
        space = self.getSize()
        self.address = self.environment.call_stack.getAddress(space)
        self.depth = self.environment.call_stack.getNestingDepth()
        self.environment.symbol_table.addSymbol(
            self.identifier, self.typename, self.address, self.depth)

    def setType(self, typename):
        self.typename = typename
                
        if self.expression is not None:
            if self.typename.getName() != self.expression.result_type.getName():
                raise C2PException("identifier '" + self.identifier + "' is assigned a value of type " + self.expression.result_type.getCSymbol() + ", while " + self.typename.getCSymbol() + " is expected")
                
        if self.is_pointer:
            self.typename.is_pointer = True
            if self.expression is not None:
                if not self.expression.result_type.is_pointer:
                    raise C2PException("identifier '" + self.identifier + "' is assigned a value of type " + self.expression.result_type.getCSymbol() + ", while " + self.typename.getCSymbol() + "* is expected")


        self.typename.array_size = self.array_size
        self.allocate()

    def getSize(self):
        if self.array_size > 0:
            return self.array_size
        else:
            return 1

    # TODO (shouldn't we add identifiers as children to ASTNodes?)
    # right now this getDisplayableText is useless since Identifier is only saved as text attribute
    # that's why AST will never show the variable names used in declaration statements
    def getDisplayableText(self):
        return "var id"

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

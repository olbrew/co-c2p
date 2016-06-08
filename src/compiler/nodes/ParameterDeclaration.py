from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class ParameterDeclaration(ASTNode):

    def __init__(self, environment, typespecifier, identifier=None):
        super().__init__(environment, SmallCParser.PARAMETERDECLARATION)

        self.typespecifier = typespecifier
        self.identifier = identifier

        if self.identifier is not None:
            # Only add named variables to the symbol table
            address = environment.call_stack.getAddress()
            depth = environment.call_stack.getNestingDepth()
            environment.symbol_table.addSymbol(self.identifier, self.typespecifier, address, depth)

    def getDisplayableText(self):
        return "parameter '" + str(self.identifier) + "'"

    def generateCode(self, out):
        return

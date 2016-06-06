from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class ParameterDeclaration(ASTNode):

    def __init__(self, ast, typespecifier, identifier=None):
        super().__init__(ast, SmallCParser.PARAMETERDECLARATION)

        self.typespecifier = typespecifier
        self.identifier = identifier

        if identifier is not None:
            # Only add named variables to the symbol table
            address = ast.call_stack.getAddress()
            depth = ast.call_stack.getNestingDepth()
            ast.symbol_table.addSymbol(self.identifier, self.typespecifier, address, depth)

    def getDisplayableText(self):
        return "parameter '" + str(self.identifier) + "'"

    def generateCode(self, out):
        return

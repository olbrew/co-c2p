from ASTNode import ASTNode


class ParameterDeclaration(ASTNode):

    def __init__(self, ast, typename, identifier=None):
        ASTNode.__init__(self, ast)

        self.typename = typename
        self.identifier = identifier

        if identifier is not None:
            # Only add named variables to the symbol table
            address = ast.call_stack.getAddress()
            depth = ast.call_stack.getNestingDepth()
            ast.symbol_table.addSymbol(identifier, typename, address, depth)

    def getDisplayableText(self):
        return "parameter '" + str(self.identifier) + "'"

    def generateCode(self, out):
        return

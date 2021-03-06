from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser
from compiler.nodes.TypeSpecifier import TypeSpecifier


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
            
            
            if isinstance(self.typespecifier, TypeSpecifier):
                size = self.typespecifier.type_object.array_size
            else:
                size = 1                
            environment.call_stack.incrementAddress(size)

    def getDisplayableText(self):
        prefix = self.typespecifier.getCSymbol()
        if self.typespecifier.is_const:
            prefix = "const " + prefix
        if self.typespecifier.is_pointer:
            prefix += "*"
        return prefix + " " + str(self.identifier)

    def generateCode(self, out):
        return

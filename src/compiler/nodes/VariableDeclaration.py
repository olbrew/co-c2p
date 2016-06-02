from compiler.ASTNode import ASTNode
from compiler.types.VoidType import VoidType
#from VariableIdentifier import VariableIdentifier


class VariableDeclaration(ASTNode):

    def __init__(self, ast, typename, variable_identifiers):
        super().__init__(ast)
    
        if isinstance(typename, VoidType):
            raise Exception("Syntax error: cannot declare a variable with void type.")
        
        self.typename = typename
        self.variable_identifiers = variable_identifiers

        for var in self.variable_identifiers:
            if var.identifier not in ast.symbol_table.stack[-1]:
                var.setType(typename)
                self.addChild(var)
            else:
                raise Exception("Syntax error: duplicate declaration of variable", var.identifier)

    def getDeclarationSize(self):
        space = 0

        for var_id in self.variable_identifiers:
            space += var_id.getSize()

        return space

    def getDisplayableText(self):
        return "var decl"

    def generateCode(self, out):
        for var_id in self.variable_identifiers:
            var_id.generateCode(out)

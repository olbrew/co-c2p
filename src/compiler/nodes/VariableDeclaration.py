from ASTNode import ASTNode
from VariableIdentifier import VariableIdentifier


class VariableDeclaration(ASTNode):

    def __init__(self, ast, typename, variable_identifiers):
        ASTNode.__init__(self, ast)

        # TODO: throw error if variable or field ‘x’ declared void

        self.typename = typename
        self.variable_identifiers = variable_identifiers

        for var in self.variable_identifiers:
            var.setType(typename)
            self.addChild(var)

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

from compiler.ASTNode import ASTNode


class TypeSpecifier(ASTNode):

    def __init__(self, ast, type_object):
        super().__init__(ast)
        self.type_object = type_object

    def getDisplayableText(self):
        return self.type_object.getName()

    def generateCode(self, out):
        pass

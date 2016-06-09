from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class TypeSpecifier(ASTNode):

    def __init__(self, environment, type_object):
        super().__init__(environment, SmallCParser.TYPESPECIFIER)
        self.type_object = type_object

    # TODO (remove?) this is useless since typespecifier is never added as a child
    def getDisplayableText(self):
        return self.type_object.getName()

    def generateCode(self, out):
        pass

from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class Statement(ASTNode):

    def __init__(self, environment):
        super().__init__(environment, SmallCParser.STATEMENT)

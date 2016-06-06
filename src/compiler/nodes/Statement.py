from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser


class Statement(ASTNode):

    def __init__(self, ast):
        super().__init__(ast, SmallCParser.STATEMENT)
        
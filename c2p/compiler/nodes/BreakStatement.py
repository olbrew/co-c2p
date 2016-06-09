from .Statement import Statement
from .ControlStructure import ControlStructure
from grammar.SmallCParser import SmallCParser


class BreakStatement(Statement):

    def __init__(self, environment):
        super().__init__(environment)
        self.type = SmallCParser.BREAKSTATEMENT

    def getDisplayableText(self):
        return "break"

    def generateCode(self, out):
        # find the owning loop / switch statement
        ast_node = self

        while not isinstance(ast_node, ControlStructure):
            ast_node = ast_node.parent
        parent_block = ast_node

        self.writeInstruction("ujp " + parent_block.getBreakLabel(), out)

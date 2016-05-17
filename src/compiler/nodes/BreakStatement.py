from .Statement import Statement
from .ControlStructure import ControlStructure


class BreakStatement(Statement):

    def __init__(self, ast):
        super().__init__(ast)

    def getDisplayableText(self):
        return "break"

    def generateCode(self, out):
        # find the owning loop / switch statement
        ast_node = self

        while not isinstance(ast_node, ControlStructure):
            ast_node = ast_node.getParent()
        parent_block = ast_node

        self.writeInstruction("ujp " + parent_block.getBreakLabel(), out)

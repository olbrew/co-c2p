from .Statement import Statement
from .ControlStructure import ControlStructure
from grammar.SmallCParser import SmallCParser


class ContinueStatement(Statement):

    def __init__(self, environment):
        super().__init__(environment)
        self.type = SmallCParser.CONTINUESTATEMENT

    def getDisplayableText(self):
        return "continue"

    def generateCode(self, out):
        # find the owning loop / switch statement
        ast_node = self

        while not isinstance(ast_node, ControlStructure):
            ast_node = ast_node.parent
        parent_block = ast_node

        # jump to the beginning of the loop and evaluate the condition
        self.writeInstruction("ujp " + parent_block.getContinueLabel(), out)

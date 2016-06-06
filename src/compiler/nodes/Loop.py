from abc import abstractmethod
from .Statement import Statement
from grammar.SmallCParser import SmallCParser


# class Loop(ABC, ControlStructure, Statement):
# Statement inherits from ASTNode which inherits from ABC
# so we leave out ABC to prevent (MRO) order TypeError
class Loop(Statement):

    def __init__(self, ast):
        super().__init__(ast)
        self.type = SmallCParser.LOOP

    @abstractmethod
    def getBreakLabel(self):
        pass

    @abstractmethod
    def getContinueLabel(self):
        pass

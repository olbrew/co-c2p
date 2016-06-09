from abc import abstractmethod
from .Statement import Statement
from grammar.SmallCParser import SmallCParser


# Statement inherits from ASTNode which inherits from ABC
# so we leave out ABC to prevent (MRO) order TypeError
class Loop(Statement):

    def __init__(self, environment):
        super().__init__(environment)
        self.type = SmallCParser.LOOP

    @abstractmethod
    def getBreakLabel(self):
        pass

    @abstractmethod
    def getContinueLabel(self):
        pass

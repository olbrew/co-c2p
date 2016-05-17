from abc import ABC, abstractmethod
# from .Statement import Statement
# from .ControlStructure import ControlStructure


# class Loop(ABC, ControlStructure, Statement):
class Loop(ABC):

    def __init__(self, ast):
        super().__init__()

    @abstractmethod
    def getBreakLabel(self):
        pass

    @abstractmethod
    def getContinueLabel(self):
        pass

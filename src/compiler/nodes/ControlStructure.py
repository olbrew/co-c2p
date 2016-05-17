from abc import ABC, abstractmethod


class ControlStructure(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def getReturnLabel(self):
        pass

    @abstractmethod
    def getContinueLabel(self):
        pass

    @abstractmethod
    def getBreakLabel(self):
        pass

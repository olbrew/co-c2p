import abc
# TODO convert to proper ABC


class ControlStructure(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def getReturnLabel(self):
        return

    @abc.abstractmethod
    def getContinueLabel(self):
        return

    @abc.abstractmethod
    def getBreakLabel(self):
        return

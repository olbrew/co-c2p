from abc import ABC, abstractmethod


class Type(ABC):

    def __init__(self):
        self.is_const = False
        self.is_pointer = False
        self.array_size = 0

    def isArray(self):
        return self.array_size > 0

    @abstractmethod
    def getName(self):
        return

    @abstractmethod
    def getCSymbol(self):
        return

    @abstractmethod
    def getPSymbol(self):
        return

    @abstractmethod
    def getPoorest(self, other_type):
        return

    @abstractmethod
    def literalToPCode(self, literal):
        return

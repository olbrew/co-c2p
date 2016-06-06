from .Type import Type


class VoidType(Type):

    def __init__(self):
        super().__init__()

    def getName(self):
        return "void"

    def getCSymbol(self):
        return "void"

    def getPSymbol(self):
        return None

    def getPoorest(self, other_type):
        return None

    def literalToPCode(self, literal):
        return None

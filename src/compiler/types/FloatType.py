from .Type import Type


class FloatType(Type):

    def __init__(self):
        Type.__init__(self)

    def getName(self):
        return "real"

    def getCSymbol(self):
        return "float"

    def getPSymbol(self):
        return "r"

    def getPoorest(self, other_type):
        return other_type

    def literalToPCode(self, literal):
        return str(literal)

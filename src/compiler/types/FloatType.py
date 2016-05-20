from .Type import Type


class FloatType(Type):

    def __init__(self):
        super().__init__()

    def getName(self):
        return "real"

    def getCSymbol(self):
        return "float"

    def getPSymbol(self):
        return "r"

    def getPoorest(self, other_type):
        return other_type

    def literalToPCode(self, literal):
        # a float may end on explicit character 'f' in smallC
        if literal[-1] is 'f':
            return str(literal[:-1])
        return str(literal)

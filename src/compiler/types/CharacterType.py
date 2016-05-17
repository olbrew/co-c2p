from .Type import Type


class CharacterType(Type):

    def __init__(self):
        Type.__init__(self)

    def getName(self):
        return "character"

    def getCSymbol(self):
        return "char"

    def getPSymbol(self):
        return "c"

    def getPoorest(self, other_type):
        if other_type.getName() == "integer":
            return self
        else:
            return other_type

    def literalToPCode(self, literal):
        return str(literal)

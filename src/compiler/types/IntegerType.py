from Type import Type

class IntegerType(Type):
    def __init__(self):
        Type.__init__(self)
        
    
    def getName(self):
        return "integer"
    
    
    def getCSymbol(self):
        return "int"
        
    
    def getPSymbol(self):
        return "i"
    
    
    def getPoorest(self, other_type):
        return other_type
    
    
    def literalToPCode(self, literal):
        return str(literal)

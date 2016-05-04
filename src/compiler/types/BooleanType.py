from Type import Type

class BooleanType(Type):
    def __init__(self):
        Type.__init__(self)
        
    
    def getName(self):
        return "boolean"
    
    
    def getCSymbol(self):
        return "bool"
        
    
    def getPSymbol(self):
        return "b"
    
    
    def getPoorest(self, other_type):
        return self
    
    
    def literalToPCode(self, literal):
        if literal > 0:
            return str(True)
        else:
            return str(False)

from abc import ABCMeta, abstractmethod
#import BooleanType

class Type():
    __metaclass__ = ABCMeta

    def __init__(self):
        self.is_const = False
        self.is_pointer = False
        self.array_size = 0

    def isArray(self):
        return self.array_size > 0
        
    def getTypeFromC(self, c_type):
        switcher = {
            "bool" : BooleanType
        }
        
        return switcher.get(c_type, lambda: "nothing")
        
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
        
        
class BooleanType(Type):
    def __init__(self):
        super().__init__()
        
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
        

class VoidType(Type):
    def __init__(self):
        Type.__init__(self)
        
    
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

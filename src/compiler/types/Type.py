import abc

class Type():
    def __init__(self):
        self.is_const = false
        self.is_pointer = false
        self.array_size = 0
    
    
    def isArray(self):
        return self.array_size > 0
        
    
    @abc.abstractmethod
    def getName(self):
        return
    
    
    @abc.abstractmethod
    def getCSymbol(self):
        return
    
    
    @abc.abstractmethod
    def getPSymbol(self):
        return
        
    @abc.abstractmethod
    def getPoorest(self, other_type):
        return
        
        
    @abc.abstractmethod
    def literalToPCode(self, literal):
        return
        
    
    def getTypeFromC(self, c_type):
        switcher = {
            "bool" : BooleanType
        }
        
        return switcher.get(c_type, lambda: "nothing")

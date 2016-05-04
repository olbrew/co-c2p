import abc

class ControlStructure():
    def __init__(self):
        pass
    
    
    @abc.abstractmethod
    def	getReturnLabel(self):
        return
        
        
    @abc.abstractmethod 
    def getContinueLabel(self):
        return
        
        
    @abc.abstractmethod 
    def getBreakLabel(self):
        return
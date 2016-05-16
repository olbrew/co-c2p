import abc
import Statement
import ControlStructure

# TODO convert to proper ABC
class Loop(Statement, ControlStructure):
    def __init__(self, ast):
        Statement.__init__(self, ast)
        
    @abstractmethod
    def getBreakLabel(self):
        return
    
    @abstractmethod    
    def getContinueLabel(self):
        return


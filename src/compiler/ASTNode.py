import abc
from antlr4 import ParserRuleContext

class ASTNode(ParserRuleContext):
    '''
        TODO
        Make this object serializable
        readObject, writeObject, storeToDisk, loadFromDisk
    '''
    
    def __init__(self, ast):
        ParserRuleContext.__init__(self)
        self.ast = ast
        
    
    def addChild(self, child):
        ParserRuleContext.addChild(self, child)
        child.parent = self


    def writeInstruction(self, payload, out):
        '''
            TODO
            save instructions into p_prog file
        '''
        print(payload)
        
    
    @abc.abstractmethod
    def	getDisplayableText(self):
        return
        
        
    @abc.abstractmethod 
    def generateCode(self, out):
        return

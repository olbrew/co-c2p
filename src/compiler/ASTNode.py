import abc
from antlr4 import *
# from antlr4 import org.antlr.v4.runtime.ParserRuleContext
# from antlr4 import org.antlr.v4.runtime.tree.ParseTree

class ASTNode(ParserRuleContext):
    '''
        TODO
        Make this object serializable
        readObject, writeObject, storeToDisk, loadFromDisk
    '''
    
    def __init__(self, ast):
        self.ast = ast
        
    
    def addChild(self, child):
        super.addChild(child)
        child.parent = self


    def writeInstruction(payload):
        '''
            TODO
            save instructions into p_prog file
        '''
        print (payload)
        
    
    @abc.abstractmethod
    def	getDisplayableText(self):
        return
        
        
    @abc.abstractmethod 
    def generateCode(self, out):
        return

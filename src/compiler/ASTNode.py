from abc import ABC, abstractmethod
from antlr4 import ParserRuleContext


class ASTNode(ABC, ParserRuleContext):
    '''
        TODO
        Make this object serializable
        readObject, writeObject, storeToDisk, loadFromDisk
    '''

    def __init__(self, ast):
        super().__init__(self)
        self.ast = ast

    def addChild(self, child):
        super().addChild(child)
        child.parent = self

    def writeInstruction(self, payload, out):
        '''
            TODO
            save instructions into p_prog file
        '''
        print(payload)

    @abstractmethod
    def getDisplayableText(self):
        pass

    @abstractmethod
    def generateCode(self, out):
        pass

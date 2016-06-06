from abc import ABC, abstractmethod
import pickle
from antlr4 import ParserRuleContext


class ASTNode(ParserRuleContext, ABC):

    def __init__(self, ast, type=0):
        super().__init__()
        self.ast = ast
        self.type = type

    def addChild(self, child):
        super().addChild(child)
        child.parent = self

    def writeInstruction(self, payload, out):
        f = open(out, 'a')
        f.write(payload + '\n')
        f.close()

    def storeASTToDisk(self):
        with open('ast.pickle', 'wb') as outfile:
            pickle.dump(self.ast, outfile, pickle.HIGHEST_PROTOCOL)

    def loadASTFromDisk(self):
        with open('ast.pickle', 'rb') as outfile:
            ast = pickle.load(outfile)
        return ast

    @abstractmethod
    def getDisplayableText(self):
        pass

    @abstractmethod
    def generateCode(self, out):
        pass

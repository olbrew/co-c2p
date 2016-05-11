# following 4 lines were necessary to import Type
import os
import sys
lib_path = os.path.abspath(os.path.join('.', 'type'))
sys.path.append(lib_path)

from AST import AST
from ASTNode import ASTNode
from Type import Type

class TypeSpecifier(ASTNode):

    def __init__(self, ast, type_object):
        ASTNode.__init__(self, ast)
        self.type_object = type_object
        
    def getDisplayableText(self):
        return self.type_object.getName()
        
    def generateCode(self, out):
        pass

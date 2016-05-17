#from compiler.ASTNode import ASTNode
#from types.Type import Type
from .Expression import Expression


class Assignment(Expression):

    def __init__(self):
        super().__init__()
        self.assignmen_type = None
        self.identifier = identifier
        self.expression = expression
        self.address = address
        self.depth = depth
        self.array_index = array_index

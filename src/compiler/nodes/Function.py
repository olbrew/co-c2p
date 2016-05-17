from compiler.ASTNode import ASTNode
# from Type import Type
from .ControlStructure import ControlStructure


class Function(ASTNode, ControlStructure):

    def __init__(self, ast, return_type, identifier, parameters, content, extern):
        super().__init__(ast)

        self.return_type = return_type
        self.identifier = identifier
        self.extern = extern
        self.parameters = parameters
        self.addChild(parameters)
        self.content = content

        if content is not None:
            self.addChild(content)

        self.depth = ast.call_stack.getNestingDepth()

    def isForwardDeclaration(self):
        return self.content is None

    def getReturnLabel(self):
        return "function_" + self.identifier + "_return"

    def getBreakLabel(self):
        return None

    def getContinueLabel(self):
        return None

    def getDisplayableText(self):
        if(self.isForwardDeclaration()):
            return "declaration of function '" + self.identifier + "'"
        return "definition of function '" + self.identifier + "'"

    def generateCode(self, out):
        # TODO
        pass

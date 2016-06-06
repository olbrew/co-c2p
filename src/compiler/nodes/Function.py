from compiler.ASTNode import ASTNode
from .ControlStructure import ControlStructure
from grammar.SmallCParser import SmallCParser
from compiler.MyErrorListener import C2PException
from compiler.types.VoidType import VoidType


class Function(ASTNode, ControlStructure):

    def __init__(self, ast, return_type, identifier, parameters_decl_list, content, extern):
        super().__init__(ast, SmallCParser.FUNCTION)
        self.return_type = return_type
        self.identifier = identifier
        self.extern = extern
        self.parameters_decl_list = parameters_decl_list
        self.addChild(parameters_decl_list)
        self.content = content
            
        if self.content is not None:
            self.addChild(self.content)
            self.validateReturnType()
        
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
        if self.isForwardDeclaration():
            return

        self.writeInstruction("function_" + self.identifier + ":", out)
        self.writeInstruction(
            "ssp " + str(5 + len(self.parameters_decl_list.parameter_list) + self.content.getVarsSize()), out)

        self.content.generateCode(out)

    '''
        Checks consistency of the function's return type.
        Expects that content is not None
    '''
    def validateReturnType(self):
        for statement in self.content.statements:
            if statement.type is SmallCParser.RETURNSTATEMENT:
                if isinstance(self.return_type, VoidType):
                    raise C2PException("return-statement with a value, in function '" + self.identifier + \
                        "' returning 'void'")
                if self.return_type.getName() != statement.expression.result_type.getName():
                    raise C2PException("In return statement of functon '" + self.identifier + \
                        "' invalid conversion from " + statement.expression.result_type.getName() + " to " + self.return_type.getName())
                        
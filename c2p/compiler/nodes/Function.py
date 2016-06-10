from compiler.ASTNode import ASTNode
from .ControlStructure import ControlStructure
from grammar.SmallCParser import SmallCParser
from compiler.MyErrorListener import C2PException
from compiler.types.VoidType import VoidType


class Function(ASTNode, ControlStructure):

    def __init__(self, environment, return_type, identifier, parameter_decl_list, content, extern):
        super().__init__(environment, SmallCParser.FUNCTION)
        self.return_type = return_type
        self.identifier = identifier
        self.extern = extern
        self.parameter_decl_list = parameter_decl_list
        self.addChild(parameter_decl_list)
        self.content = content
            
        if self.content is not None:
            self.addChild(self.content)
            self.validateReturnType()
        
        self.depth = environment.call_stack.getNestingDepth()

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
            "ssp " + str(6 + len(self.parameter_decl_list.parameter_declarations) + self.content.getVarsSize()), out)

        for arg in self.parameter_decl_list.parameter_declarations:
            arg.generateCode(out)

        self.content.generateCode(out)

    '''
        Checks consistency of the function's return type.
        Expects that content is not None
    '''
    def validateReturnType(self):
        for statement in self.content.statements:
            # find return statement
            if statement.type is SmallCParser.RETURNSTATEMENT:
                # validate functions with void as return type
                if isinstance(self.return_type, VoidType):
                    raise C2PException("return-statement with a value, in function '" + self.identifier + \
                        "' returning 'void'")

                from_type = statement.expression.result_type.getCSymbol()
                if statement.expression.result_type.is_pointer:
                    from_type += "*"
                    
                to_type = self.return_type.getCSymbol()
                if self.return_type.is_pointer:
                    to_type += "*"
                elif self.return_type.is_reference:
                    to_type += "&"
                    
                # validate expected return types (basic)
                if self.return_type.getName() != statement.expression.result_type.getName():
                    raise C2PException("In return statement of functon '" + self.identifier + \
                        "' invalid conversion from " + from_type + " to " + to_type)
                else:
                    # validate pointers
                    if self.return_type.is_pointer:
                        if statement.expression.result_type.is_pointer and not statement.expression.indirection:
                            return
                        if not statement.expression.result_type.is_pointer and statement.expression.address_of:
                            return
                        raise C2PException("Function '" + self.identifier + "' should return " + \
                            to_type + " instead of " + from_type)
                    # TODO validate references
                    #elif self.return_type.is_reference:

from compiler.ASTNode import ASTNode
from compiler.types.IntegerType import IntegerType
from grammar.SmallCParser import SmallCParser
from compiler.nodes.ParameterList import ParameterList


class IncludeDirective(ASTNode):

    def __init__(self, environment, filename):
        super().__init__(environment, SmallCParser.INCLUDEDIRECTIVE)
        self.filename = filename

        if self.filename == "stdio.h":
            address = environment.call_stack.getAddress()
            depth = environment.call_stack.getNestingDepth()
            parameter_list = ParameterList([])  # TODO arguments
            environment.symbol_table.addFunction("printf", IntegerType(), parameter_list, address, depth)
            environment.symbol_table.addFunction("scanf", IntegerType(), parameter_list, address, depth)

    def getDisplayableText(self):
        return "include '" + self.filename + "'"

    def generateCode(self, out):
        # TODO
        '''
        for include in self.included_program.includes:
            include.generateCode(out)

        for func_decl in self.included_program.function_declarations:
            func_decl.generateCode(out)
        '''
        pass

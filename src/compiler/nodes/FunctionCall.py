from .Expression import Expression
#from .ParameterList import ParameterList
from compiler.types.IntegerType import IntegerType


class FunctionCall(Expression):

    def __init__(self, ast, identifier, parameters):
        super().__init__(ast)
        self.identifier = identifier
        self.parameter_list = parameters
        print("function", self.identifier, "has", ast.symbol_table.getSymbol(self.identifier).type.getName(), "as return type.")
        self.addChild(self.parameter_list)
        self.result_type = IntegerType()

    def getDisplayableText(self):
        return "call '" + self.identifier + "'"

    def generateCode(self, out):
        arguments = self.parameter_list.arguments
        self.writeInstruction("mst 0", out)

        for arg in arguments:
            arg.generateCode(out)

        self.writeInstruction("cup " + str(len(arguments)) +
                              " function_" + self.identifier, out)

from .Expression import Expression
#from .ParameterList import ParameterList
from compiler.types.IntegerType import IntegerType


class FunctionCall(Expression):

    def __init__(self, ast, identifier, parameters):
        super().__init__(ast)
        self.identifier = identifier
        self.parameter_list = parameters
        self.addChild(self.parameter_list)
        # TODO determine correct return type of the function
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

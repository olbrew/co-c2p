from .Expression import Expression
from compiler.MyErrorListener import C2PException
from grammar.SmallCParser import SmallCParser


class FunctionCall(Expression):

    def __init__(self, environment, identifier, parameters):
        super().__init__(environment)
        self.type = SmallCParser.FUNCTIONCALL
        self.identifier = identifier
        self.parameter_list = parameters
        self.addChild(self.parameter_list)

        self.result_type = environment.symbol_table.checkFunctionSignature(self.identifier, self.parameter_list).return_type

    def getDisplayableText(self):
        return "functioncall '" + self.identifier + "'"

    def generateCode(self, out):
        self.writeInstruction("mst 0", out)

        self.parameter_list.generateCode(out)

        self.writeInstruction("cup " + str(len(arguments)) +
                              " function_" + self.identifier, out)

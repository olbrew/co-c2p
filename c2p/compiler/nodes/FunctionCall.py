from .Expression import Expression
from compiler.MyErrorListener import C2PException
from grammar.SmallCParser import SmallCParser


class FunctionCall(Expression):

    def __init__(self, ast, identifier, parameters):
        super().__init__(ast)
        self.type = SmallCParser.FUNCTIONCALL
        self.identifier = identifier
        self.parameter_list = parameters
        self.addChild(self.parameter_list)

        self.result_type = ast.symbol_table.checkFunctionSignature(self.identifier, self.parameter_list).return_type

    def getDisplayableText(self):
        return "call '" + self.identifier + "'"

    def generateCode(self, out):
        arguments = self.parameter_list.arguments
        self.writeInstruction("mst 0", out)

        for arg in arguments:
            arg.generateCode(out)

        self.writeInstruction("cup " + str(len(arguments)) +
                              " function_" + self.identifier, out)

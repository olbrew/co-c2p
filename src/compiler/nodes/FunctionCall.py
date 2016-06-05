from .Expression import Expression
from compiler.MyErrorListener import C2PException


class FunctionCall(Expression):

    def __init__(self, ast, identifier, parameters):
        super().__init__(ast)
        self.identifier = identifier

        found_identifier = False
        for scope in ast.symbol_table.stack:
            if self.identifier in scope:
                found_identifier = True
        if not found_identifier:
            raise C2PException("function '" + self.identifier +
                               "' is called before declaration / definition")

        self.parameter_list = parameters
        self.addChild(self.parameter_list)
        self.result_type = ast.symbol_table.getSymbol(self.identifier).type

    def getDisplayableText(self):
        return "call '" + self.identifier + "'"

    def generateCode(self, out):
        arguments = self.parameter_list.arguments
        self.writeInstruction("mst 0", out)

        for arg in arguments:
            arg.generateCode(out)

        self.writeInstruction("cup " + str(len(arguments)) +
                              " function_" + self.identifier, out)

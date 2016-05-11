import Expression
import IntegerType
import ParameterList

class FunctionCall(Expression):
    def __init__(self, ast, identifier, parameters):
        Expression.__init__(self, ast)
        self.identifier = identifier
        self.parameters = parameters
        self.addChild(self.parameters)    
        # TODO determine correct return type of the function
        self.result_type = IntegerType()
    
    def getDisplayableText(self):
        return "call '" + self.identifier + "'"
        
    def generateCode(self, out):
        params = parameters.getParamaters()
        self.writeInstruction("mst 0", out)
    
        for parameter in params:
            param.generateCode(out)
        
        self.writeInstruction("cup " + str(len(params)) + " function_" + self.identifier, out)

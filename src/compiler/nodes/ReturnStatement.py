import Statement
import Function
import ControlStructure
import VoidType
import AST

class ReturnStatement(Statement):
    def __init__(self, ast, expression):
        Statement.__init__(self, ast)
        self.expression = expression
        self.addChild(self.expression)
            
    def getDisplayableText(self):
        return "return"
        
    def generateCode(self, out):
        # Find the owning function
        node = self
        controlStructure = None
        while not isinstance(node, Function):
            node = node.getParent()
            if (controlStructure is None) and isinstance(node, ControlStructure):
                controlStructure = node
        function = node

        self.expression.generateCode(out)
        
        expr_type = self.expression.result_type
        return_type = function.return_type
        if not isinstance(expr_type, VoidType):
            # TODO warning for implicit cast
            if expr_type.getName() is return_type.getName():
                self.writeInstruction("conv " + expr_type.getPSymbol() + " " + return_type.getPSymbol(), out)
        
        self.writeInstruction("str " + return_type.getPSymbol() + str(self.ast.call_stack.getNestingDepth() - function.getDepth()) + " 0", out)
        self.writeInstruction("ujp " + controlStructure.getReturnLabel(), out)

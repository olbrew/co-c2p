import Statement

class IfStatement(Statement):
    label_counter = 0
    
    def __init__(self, ast, expression, if_statement):
        Statement.__init__(self, ast)
        self.expression = expression
        self.if_statement = if_statement
        self.addChild(self.expression)
        self.addChild(self.if_statement)
        
    def getDisplayableText(self):
        return "if"
        
    def generateCode(self, out):
        # First get the result of the condition on top of the stack
        self.expression.generateCode(out)
        
        # Evaluate it
        self.writeInstruction("fjp if_" + str(IfStatement.label_counter) + "_end", out)
        
        # if the condition is true, execute the statement
        self.if_statement.generateCode(out)
        self.writeInstruction("if_" + str(IfStatement.label_counter) + "_end:", out)
        
        IfStatement.label_counter += 1

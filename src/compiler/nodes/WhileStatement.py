from .Loop import Loop
from .ControlStructure import ControlStructure


class WhileStatement(Loop):
    label_counter = 0

    def __init__(self, ast, expression, statement):
        super().__init__(ast)
        self.expression = expression
        self.statement = statement
        self.addChild(expression)
        self.addChild(statement)
        self.label_id = int(WhileStatement.label_counter)
        WhileStatement.label_counter += 1

    def getBreakLabel(self):
        return "while_" + str(self.label_id) + "_end"

    def getContinueLabel(self):
        return "while_" + str(self.label_id) + "_begin"

    def getReturnLabel(self):
        node = self.parent
        while not isinstance(node, ControlStructure):
            node = node.parent
        return node.getReturnLabel()

    def getDisplayableText(self):
        return "while"

    def generateCode(self, out):
        self.expression.generateCode(out)
        self.writeInstruction("out i", out)
        self.writeInstruction("ldc c '\\n'", out)
        self.writeInstruction("out c", out)

        self.writeInstruction(
            "while_" + str(self.label_id) + "_begin:", out)
        self.expression.generateCode(out)
        self.writeInstruction(
            "fjp while_" + str(self.label_id) + "_end", out)
        self.statement.generateCode(out)
        self.writeInstruction(
            "ujp while_" + str(self.label_id) + "_begin", out)
        self.writeInstruction(
            "while_" + str(self.label_id) + "_end:", out)

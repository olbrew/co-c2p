from .Expression import Expression
from grammar.SmallCParser import SmallCParser


class Condition(Expression):

    label_counter = 0

    def __init__(self, environment, expr_disjunction, expression, expr_condition):
        super().__init__(environment)
        self.type = SmallCParser.CONDITION
        self.disjunction = expr_disjunction
        self.expression = expression
        self.condition = expr_condition
        self.addChild(self.disjunction)
        self.addChild(self.expression)
        self.addChild(self.condition)

        operand_type = self.expression.result_type.getPoorest(
            self.condition.result_type)
        self.result_type = operand_type

    def getDisplayableText(self):
        # something goes wrong if we try to output "? :" instead
        return "ternary operator"

    def generateCode(self, out):
        # first get the result of the condition on top of the stack
        self.disjunction.generateCode(out)

        # evaluate it
        self.writeInstruction(
            "fjp condition_" + str(Condition.label_counter) + "_false", out)

        # if condition is true, put the result of the lhs on top of the stack
        self.expression.generateCode(out)
        self.cast(self.expression, out)
        self.writeInstruction(
            "ujp condition_" + str(Condition.label_counter) + "_end", out)
        self.writeInstruction(
            "condition_" + str(Condition.label_counter) + "_false:", out)

        # if condition is false, put the result of the rhs on top of the stack
        self.condition.generateCode(out)
        self.cast(self.condition, out)
        self.writeInstruction(
            "condition_" + str(Condition.label_counter) + "_end:", out)

        Condition.label_counter += 1

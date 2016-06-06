from .Loop import Loop
from grammar.SmallCParser import SmallCParser


class ForStatement(Loop):
    label_counter = 0

    def __init__(self, ast, var_decl, expr_condition, expr_update, statement):
        super().__init__(ast)
        self.type = SmallCParser.FORSTATEMENT
        self.var_decl = var_decl
        self.condition = expr_condition
        self.update = expr_update
        self.statement = statement
        self.addChild(self.var_decl)
        self.addChild(self.condition)
        self.addChild(self.update)
        self.addChild(self.statement)

        self.label_id = str(ForStatement.label_counter)
        ForStatement.label_counter += 1

    def getDisplayableText(self):
        return "for"

    def getBreakLabel(self):
        return "for_" + self.label_id + "_inner_end"

    def getContinueLabel(self):
        return "for_" + self.label_id + "_continue"

    def getReturnLabel(self):
        # TODO Auto-generated method stub
        pass

    def generateCode(self, out):
        self.writeInstruction("mst 0", out)
        self.writeInstruction("cup 0 for_" + self.label_id + "_begin", out)
        self.writeInstruction("ujp for_" + self.label_id + "_end", out)
        self.writeInstruction("for_" + self.label_id + "_begin:", out)
        self.writeInstruction(
            "ssp " + str(5 + self.var_decl.getDeclarationSize()), out)

        if self.var_decl is not None:
            self.var_decl.generateCode(out)
        self.writeInstruction("for_" + self.label_id + "_inner_begin:", out)

        if self.condition is not None:
            self.condition.generateCode(out)
        else:
            self.writeInstruction("ldc i 0", out)
            self.writeInstruction("conv i b", out)
        self.writeInstruction("fjp for_" + self.label_id + "_inner_end", out)

        if self.update is not None:
            self.update.generateCode(out)
        self.writeInstruction("ujp for_" + self.label_id + "_inner_begin", out)

        self.writeInstruction("for_" + self.label_id + "_inner_end:", out)
        self.writeInstruction("retp", out)

        self.writeInstruction("for_" + self.label_id + "_end:", out)

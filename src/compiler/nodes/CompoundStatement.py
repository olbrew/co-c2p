from Statement import Statement
from ControlStructure import ControlStructure
from VariableDeclaration import VariableDeclaration


class CompoundStatement(Statement, ControlStructure):

    label_counter = 0

    def __init__(self, ast, var_decls, statements):
        Statement.__init__(self, ast)
        ControlStructure.__init__(self)

        self.var_decls = var_decls
        self.statements = statements

        for var_decl in self.var_decls:
            self.addChild(var_decl)

        for stmt in self.statements:
            self.addChild(stmt)

        self.label_id = str(CompoundStatement.label_counter)
        CompoundStatement.label_counter += 1

    def getVarsSize(self):
        space = 0
        for var_decl in self.var_decls:
            space += var_decl.getDeclarationSize()
        return space

    def getReturnLabel(self):
        # TODO: check if parent is instance of Function
        return "compound_" + self.label_id + "_return"

    def getBreakLabel(self):
        return "compound_" + self.label_id + "_break"

    def getContinueLabel(self):
        return "compound_" + self.label_id + "_continue"

    def getDisplayableText(self):
        return "compound statement"

    def generateCode(self, out):
        # TODO
        pass

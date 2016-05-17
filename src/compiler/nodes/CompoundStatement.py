from .Statement import Statement
from .ControlStructure import ControlStructure
# from .VariableDeclaration import VariableDeclaration
from .Function import Function


class CompoundStatement(Statement, ControlStructure):

    label_counter = 0

    def __init__(self, ast, var_decls, statements):
        super().__init__(ast)
        # ControlStructure.__init__(self)

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
        # TODO: self.parent or self.getParent() ? check at run time which one
        # works
        if isinstance(self.parent, Function):
            return self.parent.getReturnLabel()
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

from .Statement import Statement
from .ControlStructure import ControlStructure
from .Function import Function
from compiler.types.VoidType import VoidType
from grammar.SmallCParser import SmallCParser


class CompoundStatement(Statement, ControlStructure):

    label_counter = 0

    def __init__(self, environment, var_decls, statements):
        super().__init__(environment)
        self.type = SmallCParser.COMPOUNDSTATEMENT

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
        if isinstance(self.parent, Function):
            function = self.parent
            function_id = function.identifier

            for var_decl in self.var_decls:
                var_decl.generateCode(out)

            for stmt in self.statements:
                stmt.generateCode(out)

            # Return label
            self.writeInstruction("function_" + function_id + "_return:", out)

            if isinstance(function.return_type, VoidType):
                # Return without value
                self.writeInstruction("retp", out)
            else:
                self.writeInstruction("retf", out)

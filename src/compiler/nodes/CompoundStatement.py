from .Statement import Statement
from .ControlStructure import ControlStructure
from .Function import Function
from compiler.types.VoidType import VoidType


class CompoundStatement(Statement, ControlStructure):

    label_counter = 0

    def __init__(self, ast, var_decls, statements):
        super().__init__(ast)

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

            # TODO: Let's assume that this compound stmt is the main function's
            # body for now
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
        else:
            var_decl_count = 0
            for var_decl in self.var_decls:
                var_decl_count += var_decl.getDeclarationSize()

            parent_block = self.parent
            while not isinstance(parent_block, ControlStructure):
                parent_block = parent_block.parent

            self.writeInstruction("mst 0", out)
            self.writeInstruction("cup 0 compound_" +
                                  str(self.label_id) + "_body", out)
            self.writeInstruction("dpl i", out)
            self.writeInstruction("ldc i 0", out)
            self.writeInstruction("neq i", out)
            self.writeInstruction(
                "fjp compound_" + str(self.label_id) + "_end", out)
            self.writeInstruction("dpl i", out)
            self.writeInstruction("ldc i 1", out)
            self.writeInstruction("neq i", out)
            self.writeInstruction("fjp " + parent_block.getReturnLabel(), out)
            self.writeInstruction("ujp " + parent_block.getBreakLabel(), out)

            self.writeInstruction(
                "compound_" + str(self.label_id) + "_body:", out)
            self.writeInstruction("ssp " + str(5 + var_decl_count), out)

            # TODO: just a patch for non-function bodies; think this through!
            for var_decl in self.var_decls:
                var_decl.generateCode(out)

            for stmt in self.statements:
                stmt.generateCode(out)

            self.writeInstruction(
                "compound_" + str(self.label_id) + "_continue:", out)
            self.writeInstruction("ldc i 0", out)
            self.writeInstruction("str i 0 0", out)
            self.writeInstruction("retf", out)
            self.writeInstruction(
                "compound_" + str(self.label_id) + "_return:", out)
            self.writeInstruction("ldc i 1", out)
            self.writeInstruction("str i 0 0", out)
            self.writeInstruction("retf", out)
            self.writeInstruction(
                "compound_" + str(self.label_id) + "_break:", out)
            self.writeInstruction("ldc i 2", out)
            self.writeInstruction("str i 0 0", out)
            self.writeInstruction("retf", out)
            self.writeInstruction(
                "compound_" + str(self.label_id) + "_end:", out)

from compiler.ASTNode import ASTNode
from compiler.SymbolTable import SymbolTable
from grammar.SmallCParser import SmallCParser


class Program(ASTNode):

    def __init__(self, ast, includes, var_declarations, function_declarations):
        super().__init__(ast, SmallCParser.PROGRAM)

        if ast.symbol_table is None:
            ast.symbol_table = SymbolTable()

        self.includes = includes
        self.var_declarations = var_declarations
        self.function_declarations = function_declarations

        for include in self.includes:
            self.addChild(include)

        for var_decl in self.var_declarations:
            self.addChild(var_decl)

        for func_decl in self.function_declarations:
            self.addChild(func_decl)

    def getDisplayableText(self):
        return "program"

    def generateCode(self, out):
        self.writeInstruction("ssp 5", out)

        self.writeInstruction("ujp program", out)

        for include in self.includes:
            include.generateCode(out)

        for func_decl in self.function_declarations:
            func_decl.generateCode(out)

        self.writeInstruction("program", out)
        self.writeInstruction("mst 0", out)
        self.writeInstruction("cup 0 function_main", out)
        self.writeInstruction("hlt", out)

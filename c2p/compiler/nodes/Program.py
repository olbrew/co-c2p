from compiler.ASTNode import ASTNode
from compiler.SymbolTable import SymbolTable
from grammar.SmallCParser import SmallCParser


class Program(ASTNode):

    def __init__(self, environment, include, var_declarations, function_declarations, expressions):
        super().__init__(environment, SmallCParser.PROGRAM)

        if environment.symbol_table is None:
            environment.symbol_table = SymbolTable()

        self.include = include
        self.var_declarations = var_declarations
        self.function_declarations = function_declarations
        self.expressions = expressions

        for incl in self.include:
            self.addChild(incl)

        for var_decl in self.var_declarations:
            self.addChild(var_decl)

        for func_decl in self.function_declarations:
            self.addChild(func_decl)
            
        for expr in self.expressions:
            self.addChild(expr)

    def getDisplayableText(self):
        return "SmallC program"

    def generateCode(self, out):
        self.writeInstruction("ssp 5", out)

        self.writeInstruction("ujp program", out)

        for incl in self.include:
            incl.generateCode(out)

        for func_decl in self.function_declarations:
            func_decl.generateCode(out)
            
        for expr in self.expressions:
            expr.generateCode(out)
            
        self.writeInstruction("program", out)
        self.writeInstruction("mst 0", out)
        self.writeInstruction("cup 0 function_main", out)
        self.writeInstruction("hlt", out)

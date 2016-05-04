from AST import AST
from ASTNode import ASTNode


class Program(ASTNode):

    def __init__(self, ast, includes, function_declarations):
        super().__init__(ast)
        self.includes = []
        self.function_declarations = []

        if ast.symbol_table == None:
            print("ERROR: encountered None instead of AST")

        self.includes = includes
        self.function_declarations = function_declarations

        print("Found", len(self.includes), "includes")
        print("Found", len(self.function_declarations), "functions")

        for include in self.includes:
            print(include)
            self.addChild(include)

        for func_decl in self.function_declarations:
            self.addChild(func_decl)

    def getDisplayableText(self):
        return "program"

    def generateCode(self, out):
        print("\nGenerating Program code\n")
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

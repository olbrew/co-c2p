from AST import AST
from ASTNode import ASTNode

class Program(ASTNode):    
    def __init__(self, ast, includes, function_declarations):
        super(ast)
        self.includes = []
        self.function_declarations = []

        if ast.symbol_table == None:
            print ("ERROR: encountered None instead of AST")
            
        self.includes = includes
        self.function_declarations = function_declarations
        
        for include in self.includes:
            self.addChild(include)
            
        for func_decl in self.function_declarations:
            self.addChild(func_decl)
    
    
    def getDisplayableText(self):
        return "program"
        
        
    def generateCode():
        self.writeInstruction("ssp 5")
        
        self.writeInstruction("ujp program")
        
        for include in self.includes:
            include.generateCode()
            
        for func_decl in self.function_declarations:
            func_decl.generateCode()
        
        self.writeInstruction("program")
        self.writeInstruction("mst 0")
        self.writeInstruction("cup 0 function_main")
        self.writeInstruction("hlt")

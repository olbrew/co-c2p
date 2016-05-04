from AST import AST
from ASTNode import ASTNode
from C2P import C2P


class IncludeDirective(ASTNode):

    def __init__(self, ast, filename):
        ASTNode.__init__(self, ast)
        self.filename = filename
        self.included_ast = None

        try:
            self.included_ast = C2P.main("include/" + self.filename)

            for include in self.included_ast.includes:
                self.addChild(include)

            for func_decl in self.function_declarations:
                self.addChild(func_decl)
        except IOError:
            print("Included header: ", self.filename, "not found.")

    def getDisplayableText(self):
        return "include" + self.filename + "'"

    def generateCode(self, out):
        for include in self.included_ast.includes:
            include.generateCode(out)

        for func_decl in self.function_declarations:
            func_decl.generateCode(out)

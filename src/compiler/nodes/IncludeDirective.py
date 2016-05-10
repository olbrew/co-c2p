from ASTNode import ASTNode
from C2P import run


class IncludeDirective(ASTNode):

    def __init__(self, ast, filename):
        super().__init__(ast)
        self.filename = filename
        self.included_program = None

        try:
            self.included_program = run(
                ["", "../../include/" + self.filename, "output.p"])

            for include in self.included_program.includes:
                self.addChild(include)

            for func_decl in self.included_program.function_declarations:
                self.addChild(func_decl)
        except IOError:
            print("Included header: ", self.filename, "not found.")

    def getDisplayableText(self):
        return "include '" + self.filename + "'"

    def generateCode(self, out):
        for include in self.included_program.includes:
            include.generateCode(out)

        for func_decl in self.included_program.function_declarations:
            func_decl.generateCode(out)

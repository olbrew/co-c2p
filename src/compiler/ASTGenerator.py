from SmallCVisitor import SmallCVisitor

class ASTGenerator(SmallCVisitor):
    def __init__(self, ast, tree):
        self.ast = ast
        self.tree = tree

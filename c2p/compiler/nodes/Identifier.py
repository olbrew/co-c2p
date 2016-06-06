from .Expression import Expression
from compiler.MyErrorListener import C2PException
from grammar.SmallCParser import SmallCParser



class Identifier(Expression):

    def __init__(self, ast, name, indirection, address_of, array_index):
        super().__init__(ast)
        self.type = SmallCParser.ID
        symbol = ast.symbol_table.getSymbol(name)

        self.name = name
        self.indirection = indirection
        self.address_of = address_of
        if symbol is not None:
            self.operand_type = symbol.type
            self.result_type = self.operand_type
        else:
            raise C2PException(
                "use of undeclared identifier '" + self.name + "'")

        if self.operand_type.isArray():
            self.array_index = array_index
        else:
            self.array_index = 0

        self.address = symbol.address
        self.depth = symbol.getRelativeDepth(ast.call_stack)

        if self.indirection and not self.operand_type.is_pointer:
            raise C2PException(
                "'" + self.name + "' is not a pointer and therefore can not be dereferenced")

    def getDisplayableText(self):
        return self.name

    def generateCode(self, out):
        # Get p-code datatype for this expression
        p_type = self.operand_type.getPSymbol()

        if self.indirection:
            # TODO make sure the double space is not wrong
            self.writeInstruction(
                "lod a " + " " + str(self.depth) + " " + str(self.address), out)
            self.writeInstruction("ind " + p_type, out)
        elif self.address_of:
            self.writeInstruction(
                "lda " + str(self.depth) + " " + str(self.address), out)
        else:
            self.writeInstruction("lod" + p_type + " " + str(self.depth) +
                                  " " + str(self.address + self.array_index), out)

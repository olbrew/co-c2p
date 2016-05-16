from compiler.CallStack import CallStack
from compiler.SymbolTable import SymbolTable


class AST:

    def __init__(self):
        self.call_stack = CallStack()
        self.symbol_table = SymbolTable()

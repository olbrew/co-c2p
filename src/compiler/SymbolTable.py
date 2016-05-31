#from compiler.CallStack import CallStack


class Symbol:

    def __init__(self, typename, address, depth):
        self.type = typename
        self.address = address
        #self.value = value
        self.depth = depth

    def getRelativeDepth(self, call_stack):
        stack_depth = call_stack.getNestingDepth()
        if (stack_depth < self.depth):
            # TODO: generate error
            print("ERROR: scope of symbol is larger than stack's depth.")
        return stack_depth - self.depth


class SymbolTable:

    def __init__(self):
        self.stack = [{}]

    def addSymbol(self, name, typename, address, depth):
        self.stack[len(self.stack) - 1][name] = Symbol(typename, address, depth)

    def getSymbol(self, name):
        for dictionary in reversed(self.stack):
            if name in dictionary:
                return dictionary[name]

    def incrementScope(self):
        self.stack.append({})

    def decrementScope(self):
        self.stack.pop()

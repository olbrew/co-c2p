from compiler.MyErrorListener import C2PException
from compiler.nodes.ParameterDeclaration import ParameterDeclaration
from compiler.nodes.ParameterList import ParameterList


class Symbol:

    def __init__(self, typename, address, depth):
        self.type = typename
        self.address = address
        #self.value = value
        self.depth = depth

    def getRelativeDepth(self, call_stack):
        stack_depth = call_stack.getNestingDepth()
        if stack_depth < self.depth:
            raise C2PException("scope of symbol is larger than stack's depth")
        return stack_depth - self.depth
        
        
class Function:

    def __init__(self, return_type, arg_types, address, depth):
        self.return_type = return_type
        self.arg_types = arg_types
        self.address = address
        self.depth = depth

    def getRelativeDepth(self, call_stack):
        stack_depth = call_stack.getNestingDepth()
        if stack_depth < self.depth:
            raise C2PException("scope of function is larger than stack's depth")
        return stack_depth - self.depth


class SymbolTable:

    def __init__(self):
        self.stack = [{}]  # symbols
        self.functions = [{}]

    def addSymbol(self, name, typename, address, depth):
        self.stack[len(self.stack) - 1][name] = Symbol(typename, address, depth)

    def addFunction(self, name, return_type, parameter_list, address, depth):
        try:
            self.checkFunctionSignature(name, parameter_list, return_type)
        except C2PException:
            self.functions[len(self.functions) - 1][name] = Function(return_type, parameter_list, address, depth)
            return
            
        raise C2PException("redefinition of existing function '" + name + "'")
    
    def getSymbol(self, name):
        for dictionary in reversed(self.stack):
            if name in dictionary:
                return dictionary[name]
    
    def checkFunctionSignature(self, name, parameter_list, return_type=None):
        arg_types = []
        # TODO check call function with primary arg
        if isinstance(parameter_list, ParameterList):
            for arg in parameter_list.arguments:
                arg_types.append(arg.result_type)
        else:
            if parameter_list is not None:
                for param_decl in parameter_list:
                    arg_types.append(param_decl.typespecifier)
        
        for scope in reversed(self.functions):
            if name in scope:
                if return_type is not None:
                    if return_type.getName() != scope[name].return_type.getName():
                        continue;
                
                # check whether arg_types match
                if len(arg_types) != len(scope[name].arg_types):
                    continue
                
                isTotalMatching = True
                for i in range(len(arg_types)):
                    # check pointer attributes
                    symbol = self.getSymbol(parameter_list.arguments[i].name)
                    if scope[name].arg_types[i].typespecifier.is_pointer:
                        if symbol.type.is_pointer:
                            if parameter_list.arguments[i].indirection:
                                isTotalMatching = False
                                break
                        else:
                            if not parameter_list.arguments[i].address_of:
                                isTotalMatching = False
                                break
                    else:
                        if symbol.type.is_pointer and not parameter_list.arguments[i].indirection:
                            isTotalMatching = False
                            break
                        if not symbol.type.is_pointer and parameter_list.arguments[i].address_of:
                            isTotalMatching = False
                            break
                        
                    # check for actual type
                    if arg_types[i].getName() == scope[name].arg_types[i].typespecifier.getName():
                        continue
                    else:
                        isTotalMatching = False
                        break
                if isTotalMatching:
                    return scope[name]
                
        raise C2PException("Calling an undefined function '" + name + "'")

    def incrementScope(self):
        self.stack.append({})

    def decrementScope(self):
        self.stack.pop()

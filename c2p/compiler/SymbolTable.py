from compiler.MyErrorListener import C2PException
from compiler.nodes.ParameterDeclaration import ParameterDeclaration
from compiler.nodes.ParameterDeclarationList import ParameterDeclarationList
from compiler.nodes.ParameterList import ParameterList
from compiler.nodes.TypeSpecifier import TypeSpecifier
from grammar.SmallCParser import SmallCParser


class Symbol:
    '''
        Through self.type we can determine whether this symbol 
    is_const, is_pointer, isArray()
        In case it's an array, self.value will contain a list of 
    values (where identifiers are already resolved) of array type,
    otherwise a simple value matching its type
    '''

    def __init__(self, typename, address, depth, value):
        self.type = typename
        self.address = address
        self.depth = depth
        self.value = value

    def getRelativeDepth(self, call_stack):
        stack_depth = call_stack.getNestingDepth()
        if stack_depth < self.depth:
            raise C2PException("scope of symbol is larger than stack's depth")
        return stack_depth - self.depth


class Function:

    def __init__(self, return_type, arg_types, address, depth):
        self.return_type = return_type
        self.arg_types = []
        self.address = address
        self.depth = depth

        for arg in arg_types.parameter_declarations:
            if isinstance(arg.typespecifier, TypeSpecifier):
                self.arg_types.append(arg.typespecifier.type_object)
            else:
                self.arg_types.append(arg.typespecifier)

    def getRelativeDepth(self, call_stack):
        stack_depth = call_stack.getNestingDepth()
        if stack_depth < self.depth:
            raise C2PException(
                "scope of function is larger than stack's depth")
        return stack_depth - self.depth


class SymbolTable:

    def __init__(self):
        self.stack = [{}]  # symbols
        self.functions = [{}]

    def addSymbol(self, name, typename, address, depth, value=0):
        self.stack[len(self.stack) - 1][name] = Symbol(typename,
                                                       address, depth, value)

    def addFunction(self, name, return_type, parameter_decl_list, address, depth):
        try:
            self.checkFunctionSignature(name, parameter_decl_list, return_type)
        except C2PException:
            self.functions[len(self.functions) - 1][name] = Function(
                return_type, parameter_decl_list, address, depth)
            return

        raise C2PException("redefinition of existing function '" + name + "'")

    def getSymbol(self, name):
        for dictionary in reversed(self.stack):
            if name in dictionary:
                return dictionary[name]

    # parameters is either
    #   parameter_list in case of a function call (use .arguments)
    # parameter_declaration_list in case of a function definition (use
    # .parameter_declarations)
    def checkFunctionSignature(self, name, parameters, return_type=None):
        arg_types = []
        # prepare `arg_types` with Type objects from parameter (declaration)
        # list
        if isinstance(parameters, ParameterList):
            # function call
            for arg in parameters.arguments:
                arg_types.append(arg.result_type)
        elif isinstance(parameters, ParameterDeclarationList):
            # function definition
            if parameters is not None:
                for param_decl in parameters.parameter_declarations:
                    if isinstance(param_decl, TypeSpecifier):
                        arg_types.append(param_decl.type_object)
                    else:
                        arg_types.append(param_decl)
        else:
            raise C2PException(
                "Unexpected parameters type for function '" + name + "'")

        # try to match function signature in our symbol table
        for scope in reversed(self.functions):
            if name in scope:
                # we start by checking the return type of the function
                if return_type is not None:
                    if return_type.getName() != scope[name].return_type.getName():
                        continue

                # check whether amount of arguments is the same
                if len(arg_types) != len(scope[name].arg_types):
                    continue

                isTotalMatching = True
                for i in range(len(arg_types)):
                    # match actual Type of arguments
                    if arg_types[i].getName() == scope[name].arg_types[i].getName():
                        # check that both are either pointers or none of them
                        # are
                        if not (arg_types[i].is_pointer ^ scope[name].arg_types[i].is_pointer):
                            # this doesn't check possible indirection or references,
                            # it is left out in this stage else it would over
                            # complicate things
                            continue
                        isTotalMatching = False
                        break
                    else:
                        isTotalMatching = False
                        break

                # as long as something went wrong, keep looking up in outer
                # scope
                if isTotalMatching:
                    return scope[name]

        raise C2PException("Calling an undefined function '" + name + "'")

    def incrementScope(self):
        self.stack.append({})

    def decrementScope(self):
        self.stack.pop()

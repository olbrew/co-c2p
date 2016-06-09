from compiler.ASTNode import ASTNode
from grammar.SmallCParser import SmallCParser
from compiler.MyErrorListener import C2PException
from compiler.nodes.Primary import Primary


class VariableIdentifier(ASTNode):

    def __init__(self, environment, identifier, expression, is_pointer, is_alias, array_size, array_elements):
        super().__init__(environment, SmallCParser.VARIABLEIDENTIFIER)

        self.typename = None
        self.identifier = identifier
        self.expression = expression
        self.is_pointer = is_pointer
        self.is_alias = is_alias
        self.value = 0
        self.array_size = array_size
        self.array_elements = array_elements
        self.address = None
        self.depth = None
        
        if self.expression is not None:
            self.addChild(self.expression)
            
    def allocate(self):
        space = self.getSize()
        self.address = self.environment.call_stack.getAddress(space)
        self.depth = self.environment.call_stack.getNestingDepth()
        if self.typename.isArray():
            self.environment.symbol_table.addSymbol(
                self.identifier, self.typename, self.address, self.depth, self.array_elements)
        else:
            self.environment.symbol_table.addSymbol(
                self.identifier, self.typename, self.address, self.depth, self.value)

    def setType(self, typename):
        self.typename = typename
        self.typename.is_pointer = self.is_pointer
        self.typename.array_size = self.array_size
        
        if self.expression is not None:
            self.value = self.expression.value
            if self.typename.getName() != self.expression.result_type.getName():
                raise C2PException("identifier '" + self.identifier + "' is assigned a value of type " + self.expression.result_type.getCSymbol() + ", while " + self.typename.getCSymbol() + " is expected")
                
            if self.is_pointer:
                if not self.expression.result_type.is_pointer and not self.expression.address_of:
                    raise C2PException("identifier '" + self.identifier + "' is assigned a value of type " + self.expression.result_type.getCSymbol() + ", while " + self.typename.getCSymbol() + "* is expected")
        else:
            if self.is_pointer:
                raise C2PException("variable '" + self.identifier + "' is of type " \
                    + self.typename.getCSymbol() + "*, can't initialize pointer elements with default value.")
            else:
                # determine default value for uninitialized variable
                c_type = self.typename.getCSymbol()
                if c_type == "int":
                    self.value = 0
                elif c_type == "float":
                    self.value = 0.0
                elif c_type == "char":
                    self.value = '0'
                elif c_type == "bool":
                    self.value = False

                if not self.typename.isArray():
                    # initialize variable of basic type
                    self.addChild(Primary(self.environment, self.value))
                else:
                    for element in self.array_elements:
                        self.addChild(Primary(self.environment, element))
                    if len(self.array_elements) > self.array_size:
                        raise C2PException("Array '" + self.identifier + "' has size " + str(self.array_size) +\
                                ". You cannot fill it with " + str(len(self.array_elements)) + " elements.")
                    if len(self.array_elements) < self.array_size:
                        print("Warning: array '", self.identifier, "' has size ", self.array_size,\
                        ". Remaining elements will be filled with default values.")
                    # initialize array of basic type
                    while(len(self.array_elements) != self.array_size):
                        self.array_elements.append(self.value)
                        self.addChild(Primary(self.environment, self.value))
        
        self.allocate()

    def getSize(self):
        if self.array_size > 0:
            return self.array_size
        else:
            return 1

    def getDisplayableText(self):
        if self.array_size:
            return self.identifier + "[" + str(self.array_size) + "]"
        return self.identifier

    def generateCode(self, out):
        p_type = "a" if self.is_pointer else self.typename.getPSymbol()

        if self.expression is not None:
            self.expression.generateCode(out)
        else:
            # TODO check whether it's an array and generate necessary code for it
            self.writeInstruction("ldc " + p_type + " 0", out)

        self.writeInstruction("str " + p_type + " " +
                              str(0) + " " + str(self.address), out)

        for i in range(1, self.getSize()):
            self.writeInstruction("ldc " + p_type + " 0", out)
            self.writeInstruction("str " + p_type + " " +
                                  str(0) + " " + str(self.address + i), out)

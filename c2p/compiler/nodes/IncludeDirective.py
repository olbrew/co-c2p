from compiler.ASTNode import ASTNode
from compiler.types.IntegerType import IntegerType
from grammar.SmallCParser import SmallCParser
from compiler.nodes.ParameterDeclaration import ParameterDeclaration
from compiler.nodes.ParameterDeclarationList import ParameterDeclarationList
from compiler.types.CharacterType import CharacterType
from compiler.nodes.TypeSpecifier import TypeSpecifier


class IncludeDirective(ASTNode):

    def __init__(self, environment, filename):
        super().__init__(environment, SmallCParser.INCLUDEDIRECTIVE)
        self.filename = filename

        # add `printf` and `scanf` functions to symbol table
        if self.filename == "stdio.h":
            # int printf(char *format, ...)
            # int scanf(const char *format, ...)

            # basic support implemented,
            # accepts only one argument (format) which is an array of
            # characters
            address = environment.call_stack.getAddress()
            depth = environment.call_stack.getNestingDepth()

            typeObject = CharacterType()
            typeSpecifier = TypeSpecifier(environment, typeObject)
            typeSpecifier.type_object.is_const = False
            typeSpecifier.type_object.array_size = 1

            parameter_decl = []
            parameter_decl.append(
                ParameterDeclaration(environment, typeSpecifier))
            parameter_decl_list = ParameterDeclarationList(
                environment, parameter_decl)
            parameter_decl_list.parameter_declarations[
                0].typespecifier = typeSpecifier

            environment.symbol_table.addFunction(
                "printf", IntegerType(), parameter_decl_list, address, depth)
            # NOTE set typeSpecifier.type_object.is_const to True for scanf
            #environment.symbol_table.addFunction(
            #    "scanf", IntegerType(), parameter_decl_list, address, depth)

    def getDisplayableText(self):
        return "include '" + self.filename + "'"

    def generateCode(self, out):
        # generate p-code for printf function printing 1 character
        self.writeInstruction("function_printf:", out)
        self.writeInstruction("ssp " + str(5 + 1), out)
        self.writeInstruction("lod c 0 5", out)
        self.writeInstruction("out c", out)
        
        self.writeInstruction("ldc i 1", out)
        self.writeInstruction("str i 0 0", out)  # return amount of printed characters
        
        self.writeInstruction("ujp function_printf_return", out)
        self.writeInstruction("function_printf_return:", out)
        self.writeInstruction("retf", out)

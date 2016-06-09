from .Expression import Expression
from compiler.types.IntegerType import IntegerType
from compiler.types.FloatType import FloatType
from compiler.types.BooleanType import BooleanType
from compiler.types.CharacterType import CharacterType
from compiler.MyErrorListener import C2PException
from grammar.SmallCParser import SmallCParser


class Primary(Expression):

    def __init__(self, environment, value):
        super().__init__(environment)
        self.type = SmallCParser.PRIMARY
        
        if isinstance(value, int):
            self.value = value
            self.operand_type = IntegerType()
            self.result_type = self.operand_type
        elif isinstance(value, float):
            self.value = value
            self.operand_type = FloatType()
            self.result_type = self.operand_type
        elif isinstance(value, bool):
            if value:
                self.value = 1
            else:
                self.value = 0
            # TODO make sure operand_type is of correct type
            self.operand_type = IntegerType()
            self.result_type = BooleanType()
        elif isinstance(value, str):
            self.value = "'" + value + "'"
            self.operand_type = CharacterType()
            self.result_type = self.operand_type
        else:
            raise C2PException("use of unrecognized primary value " + str(value))

    def getDisplayableText(self):
        return self.result_type.literalToPCode(self.value)

    def generateCode(self, out):
        p_type_operand = self.operand_type.getPSymbol()
        p_type_result = self.result_type.getPSymbol()
        p_code_operand = self.operand_type.literalToPCode(self.value)
        self.writeInstruction("ldc " + p_type_operand +
                              " " + p_code_operand, out)

        # Implicitly cast boolean
        if self.operand_type.getName() is not self.result_type.getName():
            self.writeInstruction(
                "conv " + p_type_operand + " " + p_type_result, out)

from grammar.SmallCVisitor import SmallCVisitor
from grammar.SmallCParser import SmallCParser
from compiler.nodes.Program import Program
from compiler.nodes.IncludeDirective import IncludeDirective
from compiler.nodes.Function import Function
from compiler.nodes.ParameterDeclarationList import ParameterDeclarationList
from compiler.nodes.TypeSpecifier import TypeSpecifier
from compiler.nodes.CompoundStatement import CompoundStatement
from compiler.nodes.BreakStatement import BreakStatement
from compiler.nodes.ContinueStatement import ContinueStatement
from compiler.nodes.ReturnStatement import ReturnStatement
from compiler.nodes.WriteIntStatement import WriteIntStatement
from compiler.nodes.Identifier import Identifier
from compiler.nodes.ParameterDeclaration import ParameterDeclaration
from compiler.nodes.ParameterList import ParameterList
from compiler.nodes.VariableIdentifier import VariableIdentifier
from compiler.nodes.VariableDeclaration import VariableDeclaration
from compiler.nodes.IfElseStatement import IfElseStatement
from compiler.nodes.IfStatement import IfStatement
from compiler.nodes.WhileStatement import WhileStatement
from compiler.nodes.ForStatement import ForStatement
from compiler.nodes.Assignment import Assignment
from compiler.nodes.FunctionCall import FunctionCall
from compiler.nodes.Condition import Condition
from compiler.nodes.Disjunction import Disjunction
from compiler.nodes.Conjunction import Conjunction
from compiler.nodes.Comparison import Comparison
from compiler.nodes.Relation import Relation
from compiler.nodes.Equation import Equation
from compiler.nodes.Term import Term
from compiler.nodes.Factor import Factor
from compiler.nodes.Primary import Primary
from compiler.types.Type import Type
from compiler.types.IntegerType import IntegerType
from compiler.types.FloatType import FloatType
from compiler.types.CharacterType import CharacterType
from compiler.types.BooleanType import BooleanType
from compiler.types.VoidType import VoidType
from compiler.MyErrorListener import MyErrorListener, C2PException


class ASTGenerator(SmallCVisitor):

    def __init__(self, ast, parsetree):
        self.ast = ast
        self.parsetree = parsetree

    def generate(self):
        return self.visitSmallc_program(self.parsetree)

    # Visit a parse tree produced by SmallCParser#smallc_program.
    def visitSmallc_program(self, parsetree: SmallCParser.Smallc_programContext):
        include_contexts = parsetree.include()
        function_contexts = parsetree.function_definition()

        include_directives = []
        for inc_ctx in include_contexts:
            include_directives.append(self.visit(inc_ctx))

        var_decls = []
        for var_decl in parsetree.var_decl():
            var_decls.append(self.visit(var_decl))

        functions = []
        for func_ctx in function_contexts:
            functions.append(self.visit(func_ctx))

        return Program(self.ast, include_directives, var_decls, functions)

    # Visit a parse tree produced by SmallCParser#include.
    def visitInclude(self, parsetree: SmallCParser.IncludeContext):
        return IncludeDirective(self.ast, parsetree.STDIO().getText())

    # Visit a parse tree produced by SmallCParser#function_definition.
    def visitFunction_definition(self, parsetree: SmallCParser.Function_definitionContext):
        self.ast.symbol_table.incrementScope()
        self.ast.call_stack.incrementDepth()

        type_spec = self.visit(parsetree.type_specifier())
        type_object = type_spec.type_object
        
        identifier = parsetree.identifier().IDENTIFIER().getText()

        if parsetree.param_decl_list() is None:
            parameter_list = ParameterDeclarationList(self.ast, [
            ], False)
        else:
            parameter_list = self.visit(parsetree.param_decl_list())

        if parsetree.compound_stmt() is None:
            # forward declaration
            statements = None
        else:
            # function definition
            statements = self.visitCompound_stmt(parsetree.compound_stmt(), True)
        
        self.ast.call_stack.decrementDepth()
        
        # check consistency of function signature
        if type_object.getName() == "void":
            print(statements.statements)
        
        func = Function(self.ast, type_object, identifier, parameter_list,
                        statements, parsetree.EXTERN() is not None)

        self.ast.symbol_table.decrementScope()

        if self.ast.symbol_table.getSymbol(identifier) is None:
            address = self.ast.call_stack.getAddress()
            depth = self.ast.call_stack.getNestingDepth()
            self.ast.symbol_table.addSymbol(identifier, type_object, address, depth)
        
        return func

    # Visit a parse tree produced by SmallCParser#type_specifier.
    def visitType_specifier(self, parsetree: SmallCParser.Type_specifierContext):
        is_const = parsetree.CONST() is not None
        
        typetext = parsetree.getChild(int(is_const)).getText()
        if typetext == "bool":
            typename = BooleanType()
        elif typetext == "char":
            typename = CharacterType()
        elif typetext == "int":
            typename = IntegerType()
        elif typetext == "void":
            typename = VoidType()
        elif typetext == "float":
            typename = FloatType()
        else:
            line = parsetree.start.line
            column = parsetree.start.column
            msg = "'" + typename + "' is not a recognzized type"
            MyErrorListener().semanticError(line, column, msg)
        
        typename.is_const = is_const
        
        return TypeSpecifier(self.ast, typename)

    # Visit a parse tree produced by SmallCParser#compound_stmt.
    # def visitCompound_stmt(self, parsetree: SmallCParser.Compound_stmtContext):
    #    return visitCompound_stmt(parsetree, False)

    def visitCompound_stmt(self, parsetree: SmallCParser.Compound_stmtContext, isFunctionBody=False):
        self.ast.symbol_table.incrementScope()
        if not isFunctionBody:
            self.ast.call_stack.incrementDepth()

        var_decls = []
        for var_decl in parsetree.var_decl():
            var_decls.append(self.visit(var_decl))

        statements = []
        for stmt in parsetree.stmt():
            statements.append(self.visit(stmt))

        stmt = CompoundStatement(self.ast, var_decls, statements)

        if not isFunctionBody:
            self.ast.call_stack.decrementDepth()
        self.ast.symbol_table.decrementScope()
        
        return stmt

    # Visit a parse tree produced by SmallCParser#var_decl.
    def visitVar_decl(self, parsetree: SmallCParser.Var_declContext):
        type_specifier = self.visit(parsetree.type_specifier())
        type_object = type_specifier.type_object

        var_decl_list = []
        for decl in parsetree.var_decl_list().variable_id():
            var_decl_list.append(self.visit(decl))
        
        try:
            return VariableDeclaration(self.ast, type_object, var_decl_list)
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

    # Visit a parse tree produced by SmallCParser#var_decl_list.
    def visitVar_decl_list(self, parsetree: SmallCParser.Var_decl_listContext):
        return None

    # Visit a parse tree produced by SmallCParser#stmt.
    def visitStmt(self, parsetree: SmallCParser.StmtContext):
        if parsetree.compound_stmt() is not None:
            return self.visit(parsetree.compound_stmt())
        elif parsetree.cond_stmt() is not None:
            return self.visit(parsetree.cond_stmt())
        elif parsetree.while_stmt() is not None:
            return self.visit(parsetree.while_stmt())
        elif parsetree.for_stmt() is not None:
            return self.visit(parsetree.for_stmt())
        elif parsetree.expr() is not None:
            return self.visit(parsetree.expr())
        elif parsetree.BREAK() is not None:
            return BreakStatement(self.ast)
        elif parsetree.CONTINUE() is not None:
            return ContinueStatement(self.ast)
        elif parsetree.RETURN() is not None:
            expression = self.visit(parsetree.expr())
            return ReturnStatement(self.ast, expression)
        elif parsetree.WRITEINT() is not None:
            expression = self.visit(parsetree.expr())
            return WriteIntStatement(self.ast, expression)
        elif parsetree.assignment() is not None:
            return self.visit(parsetree.assignment())
        elif parsetree.functioncall() is not None:
            return self.visit(parsetree.functioncall())
        else:
            line = parsetree.start.line
            column = parsetree.start.column
            msg = "unrecognized statement"
            MyErrorListener().semanticError(line, column, msg)

    # Visit a parse tree produced by SmallCParser#identifier.
    def visitIdentifier(self, parsetree: SmallCParser.IdentifierContext):
        indirection = parsetree.ASTERIKS() is not None
        address_of = parsetree.AMPERSAND() is not None
        if parsetree.array_definition() is None:
            index = 0
        else:
            index = int(parsetree.array_definition().INTEGER().getText())

        if indirection or address_of:
            name = parsetree.getChild(1).getText()
        else:
            name = parsetree.getChild(0).getText()
        
        try:
            return Identifier(self.ast, name, indirection, address_of, index)
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

    # Visit a parse tree produced by SmallCParser#param_decl_list.
    def visitParam_decl_list(self, parsetree: SmallCParser.Param_decl_listContext):
        parameter_decl_list = []
        for param_decl in parsetree.parameter_decl():
            parameter_decl_list.append(self.visit(param_decl))

        return ParameterDeclarationList(self.ast, parameter_decl_list)

    # Visit a parse tree produced by SmallCParser#parameter_decl.
    def visitParameter_decl(self, parsetree: SmallCParser.Parameter_declContext):
        type_specifier = self.visit(parsetree.type_specifier())
        type_object = type_specifier.type_object

        if parsetree.identifier() is not None:
            type_object.is_pointer = parsetree.identifier().ASTERIKS() is not None
            type_object.is_reference = parsetree.identifier().AMPERSAND() is not None
            identifier = parsetree.identifier().IDENTIFIER().getText()
            return ParameterDeclaration(self.ast, type_object, identifier)

        return ParameterDeclaration(self.ast, type_object)

    # Visit a parse tree produced by SmallCParser#param_list.
    def visitParam_list(self, parsetree: SmallCParser.Param_listContext):
        arguments = []
        for expr in parsetree.expr():
            arguments.append(self.visit(expr))

        return ParameterList(self.ast, arguments)

    # Visit a parse tree produced by SmallCParser#variable_id.
    def visitVariable_id(self, parsetree: SmallCParser.Variable_idContext):
        is_pointer = parsetree.identifier().ASTERIKS() is not None
        is_reference = parsetree.identifier().AMPERSAND() is not None

        if parsetree.identifier().array_definition() is None:
            array_size = 0
        else:
            array_size = int(parsetree.identifier(
            ).array_definition().INTEGER().getText())

        if is_pointer or is_reference:
            identifier = parsetree.identifier().getChild(1).getText()
        else:
            identifier = parsetree.identifier().getChild(0).getText()

        if parsetree.expr() is None:
            expression = None
        else:
            expression = self.visit(parsetree.expr())

        return VariableIdentifier(self.ast, identifier, expression, is_pointer, is_reference)

    # Visit a parse tree produced by SmallCParser#cond_stmt.
    def visitCond_stmt(self, parsetree: SmallCParser.Cond_stmtContext):
        expression = self.visit(parsetree.expr())
        statement = self.visit(parsetree.stmt(0))

        if len(parsetree.stmt()) is 2:
            else_stmt = self.visit(parsetree.stmt(1))
            return IfElseStatement(self.ast, expression, statement, else_stmt)

        return IfStatement(self.ast, expression, statement)

    # Visit a parse tree produced by SmallCParser#while_stmt.
    def visitWhile_stmt(self, parsetree: SmallCParser.While_stmtContext):
        expression = self.visit(parsetree.expr())
        statement = self.visit(parsetree.stmt())
        return WhileStatement(self.ast, expression, statement)

    # Visit a parse tree produced by SmallCParser#for_stmt.
    def visitFor_stmt(self, parsetree: SmallCParser.For_stmtContext):
        self.ast.symbol_table.incrementScope()
        self.ast.call_stack.incrementDepth()

        if parsetree.var_decl_list() is not None:
            # TODO
            # ForStatement might become more complex if we allow multiple
            # variable initializations in for body
            var_decl = self.visit(parsetree.var_decl_list())
        else:
            var_decl = self.visit(parsetree.var_decl())

        condition = self.visit(parsetree.expr(0))
        update = self.visit(parsetree.expr(1))
        statement = self.visit(parsetree.stmt())
        for_stmt = ForStatement(
            self.ast, var_decl, condition, update, statement)

        self.ast.call_stack.decrementDepth()
        self.ast.symbol_table.decrementScope()

        return for_stmt

    # Visit a parse tree produced by SmallCParser#expr.
    def visitExpr(self, parsetree: SmallCParser.ExprContext):
        if parsetree.assignment() is not None:
            return self.visit(parsetree.assignment())
        elif parsetree.condition() is not None:
            return self.visit(parsetree.condition())
        elif parsetree.functioncall() is not None:
            return self.visit(parsetree.functioncall())
        else:
            line = parsetree.start.line
            column = parsetree.start.column
            msg = "unrecognized expression"
            MyErrorListener().semanticError(line, column, msg)

    # Visit a parse tree produced by SmallCParser#assignment.
    def visitAssignment(self, parsetree: SmallCParser.AssignmentContext):
        identifier = parsetree.identifier().IDENTIFIER().getText()
        expression = self.visit(parsetree.expr())

        if parsetree.identifier().array_definition() is None:
            index = 0
        else:
            index = int(parsetree.identifier(
            ).array_definition().INTEGER().getText())

        try:
            return Assignment(self.ast, identifier, expression, index)
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

    # Visit a parse tree produced by SmallCParser#functioncall.
    def visitFunctioncall(self, parsetree: SmallCParser.FunctioncallContext):
        identifier = parsetree.identifier().IDENTIFIER().getText()

        if parsetree.param_list() is None:
            parameter_list = ParameterList(self.ast, [])
        else:
            parameter_list = self.visit(parsetree.param_list())

        try:
            return FunctionCall(self.ast, identifier, parameter_list)
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

    # Visit a parse tree produced by SmallCParser#condition.
    def visitCondition(self, parsetree: SmallCParser.ConditionContext):
        if parsetree.expr() is not None:
            disjunction = self.visit(parsetree.disjunction())
            expression = self.visit(parsetree.expr())
            condition = self.visit(parsetree.condition())
            return Condition(self.ast, disjunction, expression, condition)

        return self.visit(parsetree.disjunction())

    # Visit a parse tree produced by SmallCParser#disjunction.
    def visitDisjunction(self, parsetree: SmallCParser.DisjunctionContext):
        if parsetree.disjunction() is not None:
            disjunction = self.visit(parsetree.disjunction())
            conjunction = self.visit(parsetree.conjunction())
            return Disjunction(self.ast, disjunction, conjunction)

        return self.visit(parsetree.conjunction())

    # Visit a parse tree produced by SmallCParser#conjunction.
    def visitConjunction(self, parsetree: SmallCParser.ConjunctionContext):
        if parsetree.conjunction() is not None:
            conjunction = self.visit(parsetree.conjunction())
            comparison = self.visit(parsetree.comparison())
            return Conjunction(self.ast, conjunction, comparison)

        return self.visit(parsetree.comparison())

    # Visit a parse tree produced by SmallCParser#comparison.
    def visitComparison(self, parsetree: SmallCParser.ComparisonContext):
        if len(parsetree.relation()) is 2:
            relation1 = self.visit(parsetree.relation(0))
            relation2 = self.visit(parsetree.relation(1))
            if parsetree.EQUALITY() is not None:
                operator = "=="
            else:
                operator = "!="
            try:
                return Comparison(self.ast, relation1, relation2, operator)
            except C2PException as e:
                line = parsetree.start.line
                column = parsetree.start.column
                MyErrorListener().semanticError(line, column, e.msg)

        return self.visit(parsetree.relation(0))

    # Visit a parse tree produced by SmallCParser#relation.
    def visitRelation(self, parsetree: SmallCParser.RelationContext):
        if len(parsetree.equation()) is 2:
            equation1 = self.visit(parsetree.equation(0))
            equation2 = self.visit(parsetree.equation(1))
            if parsetree.LEFTANGLE() is not None:
                operator = "<"
            else:
                operator = ">"
            try:
                return Relation(self.ast, equation1, equation2, operator)
            except C2PException as e:
                line = parsetree.start.line
                column = parsetree.start.column
                MyErrorListener().semanticError(line, column, e.msg)

        return self.visit(parsetree.equation(0))

    # Visit a parse tree produced by SmallCParser#equation.
    def visitEquation(self, parsetree: SmallCParser.EquationContext):
        if parsetree.equation() is not None:
            equation = self.visit(parsetree.equation())
            term = self.visit(parsetree.term())
            if parsetree.MINUS() is None:
                operator = parsetree.PLUS().getText()
            else:
                operator = parsetree.MINUS().getText()
            try:
                return Equation(self.ast, equation, term, operator)
            except C2PException as e:
                line = parsetree.start.line
                column = parsetree.start.column
                MyErrorListener().semanticError(line, column, e.msg)

        return self.visit(parsetree.term())

    # Visit a parse tree produced by SmallCParser#term.
    def visitTerm(self, parsetree: SmallCParser.TermContext):
        if parsetree.term() is not None:
            term = self.visit(parsetree.term())
            factor = self.visit(parsetree.factor())
            operator = "*"
            if parsetree.SLASH() is not None:
                operator = "/"
            elif parsetree.PROCENT() is not None:
                operator = "%"
            try:
                return Term(self.ast, term, factor, operator)
            except C2PException as e:
                line = parsetree.start.line
                column = parsetree.start.column
                MyErrorListener().semanticError(line, column, e.msg)

        return self.visit(parsetree.factor())

    # Visit a parse tree produced by SmallCParser#factor.
    def visitFactor(self, parsetree: SmallCParser.FactorContext):
        if parsetree.factor() is not None:
            factor = self.visit(parsetree.factor())
            if parsetree.EXCLAMATIONMARK() is None:
                operator = "-"
            else:
                operator = "!"
            try:
                return Factor(self.ast, factor, operator)
            except C2PException as e:
                line = parsetree.start.line
                column = parsetree.start.column
                MyErrorListener().semanticError(line, column, e.msg)

        return self.visit(parsetree.primary())

    # Visit a parse tree produced by SmallCParser#primary.
    def visitPrimary(self, parsetree: SmallCParser.PrimaryContext):
        try:
            if parsetree.INTEGER() is not None:
                value = int(parsetree.INTEGER().getText())
                return Primary(self.ast, value)
            elif parsetree.REAL() is not None:
                real = parsetree.REAL().getText()
                if real[-1] is 'f':
                    real = real[:-1]
                value = float(real)
                return Primary(self.ast, value)
            elif parsetree.CHARCONST() is not None:
                # TODO: use chars correctly
                value = parsetree.CHARCONST().getText()
                return Primary(self.ast, value[0])
            elif parsetree.BOOLEAN() is not None:
                value = parsetree.BOOLEAN().getText() is "True"
                return Primary(self.ast, value)
            elif parsetree.identifier() is not None:
                return self.visit(parsetree.identifier())
            elif parsetree.expr() is not None:
                return self.visit(parsetree.expr())
            elif parsetree.functioncall() is not None:
                return self.visit(parsetree.functioncall())
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)
        line = parsetree.start.line
        column = parsetree.start.column
        msg = "unrecognized primary"
        MyErrorListener().semanticError(line, column, msg)
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
from compiler.nodes.VariableDeclarationList import VariableDeclarationList
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
from compiler.types.IntegerType import IntegerType
from compiler.types.FloatType import FloatType
from compiler.types.CharacterType import CharacterType
from compiler.types.BooleanType import BooleanType
from compiler.types.VoidType import VoidType
from compiler.MyErrorListener import MyErrorListener, C2PException


class ASTGenerator(SmallCVisitor):

    def __init__(self, environment, parsetree):
        self.environment = environment
        self.parsetree = parsetree

    def generate(self):
        return self.visitSmallc_program(self.parsetree)

    # Visit a parse tree produced by SmallCParser#smallc_program.
    def visitSmallc_program(self, parsetree: SmallCParser.Smallc_programContext):
        include_contexts = parsetree.include()
        variable_decl_contexts = parsetree.var_decl()
        function_contexts = parsetree.function_definition()
        expression_contexts = parsetree.expr()

        include_directives = []
        if include_contexts is not None:
            for inc_ctx in include_contexts:
                include_directives.append(self.visit(inc_ctx))
        
        var_decls = []
        for var_decl in variable_decl_contexts:
            var_decls.append(self.visit(var_decl))

        functions = []
        for func_ctx in function_contexts:
            functions.append(self.visit(func_ctx))
            
        expressions = []
        for expr_ctx in expression_contexts:
            expressions.append(self.visit(expr_ctx))
        
        return Program(self.environment, include_directives, var_decls, functions, expressions)

    # Visit a parse tree produced by SmallCParser#include.
    def visitInclude(self, parsetree: SmallCParser.IncludeContext):
        return IncludeDirective(self.environment, parsetree.STDIO().getText())

    # Visit a parse tree produced by SmallCParser#function_definition.
    def visitFunction_definition(self, parsetree: SmallCParser.Function_definitionContext):
        self.environment.symbol_table.incrementScope()
        self.environment.call_stack.incrementDepth()

        type_spec = self.visit(parsetree.type_specifier())
        return_type = type_spec.type_object

        identifier = parsetree.identifier()
        func_name = identifier.IDENTIFIER().getText()
        return_type.is_pointer = identifier.ASTERIKS() is not None
        return_type.is_reference = identifier.AMPERSAND() is not None
        
        if parsetree.param_decl_list() is None:
            parameter_decl_list = ParameterDeclarationList(self.environment, [])
        else:
            parameter_decl_list = self.visit(parsetree.param_decl_list())

        if parsetree.compound_stmt() is None:
            # forward declaration
            statements = None
        else:
            # function definition
            statements = self.visitCompound_stmt(
                parsetree.compound_stmt(), True)

        self.environment.call_stack.decrementDepth()

        try:
            func = Function(self.environment, return_type, func_name, parameter_decl_list,
                        statements, parsetree.EXTERN() is not None)
            
            address = self.environment.call_stack.getAddress()
            depth = self.environment.call_stack.getNestingDepth()
            self.environment.symbol_table.addFunction(
                    func_name, return_type, func.parameter_decl_list.parameter_list, address, depth)
            
            return func
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

        self.environment.symbol_table.decrementScope()

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
            msg = "'" + typename + "' is not a recognized type"
            MyErrorListener().semanticError(line, column, msg)

        typename.is_const = is_const

        return TypeSpecifier(self.environment, typename)

    # Visit a parse tree produced by SmallCParser#compound_stmt.
    # def visitCompound_stmt(self, parsetree: SmallCParser.Compound_stmtContext):
    #    return visitCompound_stmt(parsetree, False)

    def visitCompound_stmt(self, parsetree: SmallCParser.Compound_stmtContext, isFunctionBody=False):
        self.environment.symbol_table.incrementScope()
        if not isFunctionBody:
            self.environment.call_stack.incrementDepth()

        var_decls = []
        for var_decl in parsetree.var_decl():
            var_decls.append(self.visit(var_decl))

        statements = []
        for stmt in parsetree.stmt():
            statements.append(self.visit(stmt))

        compound_stmt = CompoundStatement(self.environment, var_decls, statements)

        if not isFunctionBody:
            self.environment.call_stack.decrementDepth()
        self.environment.symbol_table.decrementScope()

        return compound_stmt

    # Visit a parse tree produced by SmallCParser#var_decl.
    def visitVar_decl(self, parsetree: SmallCParser.Var_declContext):
        type_specifier = self.visit(parsetree.type_specifier())
        type_object = type_specifier.type_object

        var_decl_list = self.visit(parsetree.var_decl_list())
        
        try:
            return VariableDeclaration(self.environment, type_object, var_decl_list)
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

    # Visit a parse tree produced by SmallCParser#var_decl_list.
    def visitVar_decl_list(self, parsetree: SmallCParser.Var_decl_listContext):
        var_list = []
        for var_id in parsetree.variable_id():
            var_list.append(self.visit(var_id))
        
        return VariableDeclarationList(self.environment, var_list)

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
        elif parsetree.BREAK() is not None:
            return BreakStatement(self.environment)
        elif parsetree.CONTINUE() is not None:
            return ContinueStatement(self.environment)
        elif parsetree.RETURN() is not None:
            expression = self.visit(parsetree.expr())
            return ReturnStatement(self.environment, expression)
        elif parsetree.expr() is not None:
            return self.visit(parsetree.expr())
        # TODO: check for parsetree.READINT(), see grammar
        elif parsetree.WRITEINT() is not None:
            expression = self.visit(parsetree.expr())
            return WriteIntStatement(self.environment, expression)
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
        
        if parsetree.array_indexing() is None:
            array_size = 0
        else:
            # TODO we assumed this is an integer
            array_size = int(parsetree.array_indexing().expr().getText())

        if indirection or address_of:
            name = parsetree.getChild(1).getText()
        else:
            name = parsetree.getChild(0).getText()
            
        try:
            return Identifier(self.environment, name, indirection, address_of, array_size)
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

    # Visit a parse tree produced by SmallCParser#param_decl_list.
    def visitParam_decl_list(self, parsetree: SmallCParser.Param_decl_listContext):
        parameter_decl_list = []
        for param_decl in parsetree.parameter_decl():
            parameter_decl_list.append(self.visit(param_decl))

        return ParameterDeclarationList(self.environment, parameter_decl_list)

    # Visit a parse tree produced by SmallCParser#parameter_decl.
    def visitParameter_decl(self, parsetree: SmallCParser.Parameter_declContext):
        type_specifier = self.visit(parsetree.type_specifier())
        type_object = type_specifier.type_object

        if parsetree.identifier() is not None:
            type_object.is_pointer = parsetree.identifier().ASTERIKS() is not None
            type_object.is_reference = parsetree.identifier().AMPERSAND() is not None
            identifier = parsetree.identifier().IDENTIFIER().getText()
            return ParameterDeclaration(self.environment, type_object, identifier)

        return ParameterDeclaration(self.environment, type_object)

    # Visit a parse tree produced by SmallCParser#param_list.
    def visitParam_list(self, parsetree: SmallCParser.Param_listContext):
        arguments = []
        for expr in parsetree.expr():
            arguments.append(self.visit(expr))

        return ParameterList(self.environment, arguments)

    # Visit a parse tree produced by SmallCParser#variable_id.
    def visitVariable_id(self, parsetree: SmallCParser.Variable_idContext):
        is_pointer = parsetree.identifier().ASTERIKS() is not None
        is_alias = parsetree.identifier().AMPERSAND() is not None
        
        if parsetree.identifier().array_indexing() is None:
            array_size = 0
        else:
            # TODO we assumed this is an integer
            array_size = int(parsetree.identifier(
            ).array_indexing().expr().getText())

        if is_pointer or is_alias:
            identifier = parsetree.identifier().getChild(1).getText()
        else:
            identifier = parsetree.identifier().getChild(0).getText()

        if parsetree.expr() is None:
            expression = None
        else:
            expression = self.visit(parsetree.expr())

        return VariableIdentifier(self.environment, identifier, expression, is_pointer, is_alias, array_size)

    # Visit a parse tree produced by SmallCParser#cond_stmt.
    def visitCond_stmt(self, parsetree: SmallCParser.Cond_stmtContext):
        expression = self.visit(parsetree.expr())
        statement = self.visit(parsetree.stmt(0))

        if len(parsetree.stmt()) == 2:
            else_stmt = self.visit(parsetree.stmt(1))
            return IfElseStatement(self.environment, expression, statement, else_stmt)

        return IfStatement(self.environment, expression, statement)

    # Visit a parse tree produced by SmallCParser#while_stmt.
    def visitWhile_stmt(self, parsetree: SmallCParser.While_stmtContext):
        # TODO increment / decrement scope and depth like in visitFor_stmt
        expression = self.visit(parsetree.expr())
        statement = self.visit(parsetree.stmt())
        return WhileStatement(self.environment, expression, statement)

    # Visit a parse tree produced by SmallCParser#for_stmt.
    def visitFor_stmt(self, parsetree: SmallCParser.For_stmtContext):
        self.environment.symbol_table.incrementScope()
        self.environment.call_stack.incrementDepth()

        # TODO verify it works (it should either allow var_decl | var_decl_list as for_init_list)
        if parsetree.var_decl() is not None:
            variable_declaration = self.visit(parsetree.var_decl())
            var_decl_list = variable_declaration.variable_identifiers
        else:
            var_decl_list = self.visit(parsetree.var_decl_list())

        condition = self.visit(parsetree.expr(0))
        update = self.visit(parsetree.expr(1))
        statement = self.visit(parsetree.stmt())
        for_stmt = ForStatement(
            self.environment, var_decl_list, condition, update, statement)

        self.environment.call_stack.decrementDepth()
        self.environment.symbol_table.decrementScope()

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
        #identifier = parsetree.identifier().IDENTIFIER().getText()
        identifier = self.visit(parsetree.identifier())
        expression = self.visit(parsetree.expr())

        try:
            return Assignment(self.environment, identifier, expression)
        except C2PException as e:
            line = parsetree.start.line
            column = parsetree.start.column
            MyErrorListener().semanticError(line, column, e.msg)

    # Visit a parse tree produced by SmallCParser#functioncall.
    def visitFunctioncall(self, parsetree: SmallCParser.FunctioncallContext):
        identifier = parsetree.identifier().IDENTIFIER().getText()

        if parsetree.param_list() is None:
            parameter_list = ParameterList(self.environment, [])
        else:
            parameter_list = self.visit(parsetree.param_list())

        try:
            return FunctionCall(self.environment, identifier, parameter_list)
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
            return Condition(self.environment, disjunction, expression, condition)

        return self.visit(parsetree.disjunction())

    # Visit a parse tree produced by SmallCParser#disjunction.
    def visitDisjunction(self, parsetree: SmallCParser.DisjunctionContext):
        if parsetree.disjunction() is not None:
            disjunction = self.visit(parsetree.disjunction())
            conjunction = self.visit(parsetree.conjunction())
            return Disjunction(self.environment, disjunction, conjunction)

        return self.visit(parsetree.conjunction())

    # Visit a parse tree produced by SmallCParser#conjunction.
    def visitConjunction(self, parsetree: SmallCParser.ConjunctionContext):
        if parsetree.conjunction() is not None:
            conjunction = self.visit(parsetree.conjunction())
            comparison = self.visit(parsetree.comparison())
            return Conjunction(self.environment, conjunction, comparison)

        return self.visit(parsetree.comparison())

    # Visit a parse tree produced by SmallCParser#comparison.
    def visitComparison(self, parsetree: SmallCParser.ComparisonContext):
        if len(parsetree.relation()) == 2:
            relation1 = self.visit(parsetree.relation(0))
            relation2 = self.visit(parsetree.relation(1))
            if parsetree.EQUALITY() is not None:
                operator = parsetree.EQUALITY().getText()
            else:
                operator = parsetree.NEQUALITY().getText()
            try:
                return Comparison(self.environment, relation1, relation2, operator)
            except C2PException as e:
                line = parsetree.start.line
                column = parsetree.start.column
                MyErrorListener().semanticError(line, column, e.msg)

        return self.visit(parsetree.relation(0))

    # Visit a parse tree produced by SmallCParser#relation.
    def visitRelation(self, parsetree: SmallCParser.RelationContext):
        if len(parsetree.equation()) == 2:
            equation1 = self.visit(parsetree.equation(0))
            equation2 = self.visit(parsetree.equation(1))
            if parsetree.LEFTANGLE() is not None:
                operator = parsetree.LEFTANGLE().getText()
            else:
                operator = parsetree.RIGHTANGLE().getText()
            try:
                return Relation(self.environment, equation1, equation2, operator)
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
                return Equation(self.environment, equation, term, operator)
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
            if parsetree.SLASH() is not None:
                operator = parsetree.SLASH().getText()
            elif parsetree.PROCENT() is not None:
                operator = parsetree.PROCENT().getText()
            else:
                operator = parsetree.ASTERIKS().getText()
            try:
                return Term(self.environment, term, factor, operator)
            except C2PException as e:
                line = parsetree.start.line
                column = parsetree.start.column
                MyErrorListener().semanticError(line, column, e.msg)

        return self.visit(parsetree.factor())

    # Visit a parse tree produced by SmallCParser#factor.
    def visitFactor(self, parsetree: SmallCParser.FactorContext):
        if parsetree.factor() is not None:
            factor = self.visit(parsetree.factor())
            if parsetree.EXCLAMATIONMARK() is not None:
                operator = parsetree.EXCLAMATIONMARK().getText()
            else:
                operator = parsetree.MINUS().getText()
            try:
                return Factor(self.environment, factor, operator)
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
                return Primary(self.environment, value)
            elif parsetree.REAL() is not None:
                real = parsetree.REAL().getText()
                value = float(real[:-1])  # skip ending 'f' literal
                return Primary(self.environment, value)
            elif parsetree.CHARCONST() is not None:
                value = parsetree.CHARCONST().getText()
                # We are interested in the first character after the quotation mark
                return Primary(self.environment, value[1])
            elif parsetree.BOOLEAN() is not None:
                value = parsetree.BOOLEAN().getText() == "true"
                return Primary(self.environment, value)
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

    '''
    # Visit a parse tree produced by SmallCParser#array.
    def visitArray(self, parsetree:SmallCParser.ArrayContext):
        is_initialization = parsetree.type_specifier() is not None
        
        if is_initialization:
            typeSpecifier = self.visit(parsetree.type_specifier())
            identifier = self.visit(parsetree.identifier())
        
            arrayInit = self.visit(parsetree.array_init())
            return Array(typeSpecifier, identifier, arrayInit)
        else:
            #indexing
        
    # Visit a parse tree produced by SmallCParser#array_init.
    # returns Array_init node with amount of elements of the array and its elements
    def visitArray_init(self, parsetree:SmallCParser.Array_initContext):
        parsetree.getChildCount()
        
            # isinstance variable id / primary
        
        
        return self.visitChildren(parsetree)

    # Visit a parse tree produced by SmallCParser#array_indexing.
    def visitArray_indexing(self, parsetree:SmallCParser.Array_indexingContext):
        return self.visitChildren(parsetree)
    '''

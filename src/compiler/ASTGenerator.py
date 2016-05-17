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
        print("Found include directives in ASTGenerator: ", include_directives)

        functions = []
        for func_ctx in function_contexts:
            print(func_ctx.getText())
            functions.append(self.visit(func_ctx))
        print("Found functions in ASTGenerator: ", functions)

        return Program(self.ast, include_directives, functions)

    # Visit a parse tree produced by SmallCParser#include.
    def visitInclude(self, parsetree: SmallCParser.IncludeContext):
        return IncludeDirective(self.ast, parsetree.FILENAME().getText())

    # Visit a parse tree produced by SmallCParser#function_definition.
    def visitFunction_definition(self, parsetree: SmallCParser.Function_definitionContext):
        self.ast.symbol_table.incrementScope()
        self.ast.call_stack.incrementDepth()

        type_spec = self.visit(parsetree.type_specifier())
        print("Type Specificier", type_spec)
        type_object = type_spec.type_object
        print("Type Object", type_object)

        identifier = parsetree.identifier().IDENTIFIER().getText()

        if parsetree.param_decl_list() is None:
            parameter_list = ParameterDeclarationList.ParameterDeclarationList(self.ast, [
            ], False)
        else:
            parameter_list = self.visit(parsetree.param_decl_list())

        print(parsetree.compound_stmt().getText())
        if parsetree.compound_stmt() is None:
            statement = None
        else:
            statement = self.visitCompound_stmt(parsetree.compound_stmt(), True)

        self.ast.call_stack.decrementDepth()

        func = Function.Function(self.ast, type_object, identifier, parameter_list,
                                 statement, parsetree.EXTERN() is not None)

        self.ast.symbol_table.decrementScope()

        return func

    # Visit a parse tree produced by SmallCParser#type_specifier.
    def visitType_specifier(self, parsetree: SmallCParser.Type_specifierContext):
        is_const = parsetree.CONST() is not None
        typename = Type.Type().getTypeFromC(parsetree.getChild(int(is_const)).getText())
        if is_const:
            typename.is_const = True
        return TypeSpecifier(self.ast, typename)

    # Visit a parse tree produced by SmallCParser#compound_stmt.
    def visitCompound_stmt(self, parsetree: SmallCParser.Compound_stmtContext):
        return visitCompound_stmt(parsetree, False)

    def visitCompound_stmt(self, parsetree: SmallCParser.Compound_stmtContext, functionBody):
        self.ast.symbol_table.incrementScope()
        if functionBody != True:
            self.ast.call_stack.incrementDepth()

        var_decls = []
        for var_decl in parsetree.var_decl():
            var_decls.append(self.visit(var_decl))

        statements = []
        for stmt in parsetree.stmt():
            statements.append(self.visit(stmt))

        stmt = CompoundStatement.CompoundStatement(
            self.ast, var_decls, statements)

        if functionBody != True:
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

        return VariableDeclaration.VariableDeclaration(self.ast, type_object, var_decl_list)

    # Visit a parse tree produced by SmallCParser#var_decl_list.
    def visitVar_decl_list(self, parsetree: SmallCParser.Var_decl_listContext):
        return None

    # Visit a parse tree produced by SmallCParser#stmt.
    def visitStmt(self, parsetree: SmallCParser.StmtContext):
        # TODO: differentiate between more statements!
        if parsetree.compound_stmt() is not None:
            return self.visit(parsetree.compound_stmt())
        elif parsetree.cond_stmt() is not None:
            return self.visit(parsetree.cond_stmt())
        elif parsetree.while_stmt() is not None:
            return self.visit(parsetree.while_stmt())
        elif parsetree.for_stmt() is not None:
            return self.visit(parsetree.for_stmt())
        elif parsetree.BREAK() is not None:
            return BreakStatement.BreakStatement(self.ast)
        elif parsetree.CONTINUE() is not None:
            return ContinueStatement.ContinueStatement(self.ast)
        elif parsetree.RETURN() is not None:
            expression = self.visit(parsetree.expr())
            return ReturnStatement.ReturnStatement(self.ast, expression)
        elif parsetree.WRITEINT() is not None:
            expression = self.visit(parsetree.expr())
            return WriteIntStatement(self.ast, expression)
        elif parsetree.assignment() is not None:
            return self.visit(parsetree.assignment())
        elif parsetree.functioncall() is not None:
            return self.visit(parsetree.functioncall())

        # TODO: throw compiler error
        return None

    # Visit a parse tree produced by SmallCParser#identifier.
    def visitIdentifier(self, parsetree: SmallCParser.IdentifierContext):
        indirection = parsetree.ASTERISK() is not None
        address_of = parsetree.AMPERSAND() is not None
        if parsetree.array_definition() is None:
            index = 0
        else:
            index = int(parsetree.array_definition().INTEGER().getText())

        if indirection or address_of:
            name = parsetree.getChild(1).getText()
        else:
            name = parsetree.getChild(0).getText()

        return Identifier(self.ast, name, indirection, address_of, index)

    # Visit a parse tree produced by SmallCParser#param_decl_list.
    def visitParam_decl_list(self, parsetree: SmallCParser.Param_decl_listContext):
        parameter_decl_list = []
        for param_decl in parsetree.parameter_decl():
            parameter_decl_list.append(self.visit(param_decl))

        return ParameterDeclarationList(self.ast, parameter_decl_list, parsetree.parameter_pack() is not None)

    # Visit a parse tree produced by SmallCParser#parameter_pack.
    def visitParameter_pack(self, parsetree: SmallCParser.Parameter_packContext):
        # TODO
        pass

    # Visit a parse tree produced by SmallCParser#parameter_decl.
    def visitParameter_decl(self, parsetree: SmallCParser.Parameter_declContext):
        type_specifier = self.visit(parsetree.type_specifier())
        type_object = type_specifier.type_object

        if parsetree.identifier() is not None:
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
        is_pointer = parsetree.identifier().ASTERISK() is not None
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

        if len(parsetree.stmt()) == 2:
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

        var_decl = self.visit(parsetree.var_decl())
        # TODO check whether we need to use var_decl() or var_decl_list()
        # ForStatement might become more complex if we allow multiple variable initializations in for body
        # var_decl_list = self.visit(parsetree.var_decl_list())
        condition = self.visit(parsetree.expr(0))
        update = self.visit(parsetree.expr(1))
        statement = self.visit(parsetree.stmt())
        for_stmt = ForStatement.ForStatement(
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

        # TODO throw compiler error
        return None

    # Visit a parse tree produced by SmallCParser#assignment.
    def visitAssignment(self, parsetree: SmallCParser.AssignmentContext):
        identifier = parsetree.identifier().IDENTIFIER().getText()
        expression = self.visit(parsetree.expr())

        if parsetree.identifier().array_definition() is None:
            index = 0
        else:
            index = int(parsetree.identifier(
            ).array_definition().INTEGER().getText())

        return Assignment.Assignment(self.ast, identifier, expression, index)

    # Visit a parse tree produced by SmallCParser#functioncall.
    def visitFunctioncall(self, parsetree: SmallCParser.FunctioncallContext):
        identifier = parsetree.identifier().IDENTIFIER().getText()

        if parsetree.param_list() is None:
            parameter_list = ParameterList.ParameterList(self.ast, [])
        else:
            parameter_list = self.visit(parsetree.param_list())

        return FunctionCall(self.ast, identifier, parameter_list)

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
        if parsetree.conjunction is not None:
            conjunction = self.visit(parsetree.conjunction())
            comparison = self.visit(parsetree.comparison())
            return Conjunction(self.ast, conjunction, comparison)

        return self.visit(parsetree.comparison())

    # Visit a parse tree produced by SmallCParser#comparison.
    def visitComparison(self, parsetree: SmallCParser.ComparisonContext):
        if len(parsetree.relation()) == 2:
            relation1 = self.visit(parsetree.relation(0))
            relation2 = self.visit(parsetree.relation(1))
            if parsetree.EQUALITY() is not None:
                operator = "=="
            else:
                operator = "!="
            return Comparison(self.ast, relation1, relation2, operator)

        return self.visit(parsetree.relation(0))

    # Visit a parse tree produced by SmallCParser#relation.
    def visitRelation(self, parsetree: SmallCParser.RelationContext):
        if len(parsetree.equation()) == 2:
            equation1 = self.visit(parsetree.equation(0))
            equation2 = self.visit(parsetree.equation(1))
            if parsetree.LEFTANGLE() is not None:
                operator = "<"
            else:
                operator = ">"
            return Relation(self.ast, equation1, equation2, operator)

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
            return Equation.Equation(self.ast, equation, term, operator)

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
            return Term.Term(self.ast, term, factor, operator)

        return self.visit(parsetree.factor())

    # Visit a parse tree produced by SmallCParser#factor.
    def visitFactor(self, parsetree: SmallCParser.FactorContext):
        if parsetree.factor() is not None:
            factor = self.visit(parsetree.factor())
            if parsetree.EXCLAMATIONMARK() is None:
                operator = "-"
            else:
                operator = "!"
            return Factor(self.ast, factor, operator)

        return self.visit(parsetree.primary())

    # Visit a parse tree produced by SmallCParser#primary.
    def visitPrimary(self, parsetree: SmallCParser.PrimaryContext):
        if parsetree.INTEGER() is not None:
            value = int(parsetree.INTEGER().getText())
            return Primary.Primary(self.ast, value)
        elif parsetree.REAL() is not None:
            value = float(parsetree.REAL().getText())
        elif parsetree.CHARCONST() is not None:
            # TODO: use chars correctly
            value = parsetree.CHARCONST().getText()
            return Primary.Primary(self.ast, value[0])
        elif parsetree.BOOLEAN() is not None:
            value = parsetree.BOOLEAN().getText() is "True"
            return Primary.Primary(self.ast, value)
        elif parsetree.identifier() is not None:
            return self.visit(parsetree.identifier())
        elif parsetree.expr() is not None:
            return self.visit(parsetree.expr())
        elif parsetree.functioncall() is not None:
            return self.visit(parsetree.functioncall())

        # TODO throw compiler error
        return None

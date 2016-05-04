# following 4 lines were necessary to import Program
import os
import sys
lib_path = os.path.abspath(os.path.join('.', 'nodes'))
sys.path.append(lib_path)

from SmallCVisitor import SmallCVisitor
from Program import Program

class ASTGenerator(SmallCVisitor):
    def __init__(self, ast, parsetree):
        self.ast = ast
        self.parsetree = parsetree
        
        
    def generate(self):
        return self.visit_smallc_program()
            
    
    def visit_smallc_program(self):
        include_contexts = self.parsetree.include()
        function_contexts = self.parsetree.function_definition()

        include_directives = []
        for inc_ctx in include_contexts:
            #print("for loop:", inc_ctx.getText())
            include_directives.append(self.visit(inc_ctx))
        print(include_directives)
        
        '''
        functions = []
        for func_ctx in function_contexts:
            # print(func_ctx.getText())
            # print(self.visit(func_ctx))
            functions.append(self.visit(func_ctx))
        print(functions)
        '''
        
        return Program(self.ast, include_directives, functions)
	
    
    def visit_function_definition(self, ctx):
        self.ast.symbol_table.incrementScope()
        self.ast.call_stack.incrementDepth()
        '''
        type_spec = self.visit(ctx.type_specifier())
        type_name = type_spec.getType()
        
        identifier = ctx.id().IDENTIFIER().getText()

        
            TODO
			ParameterDeclarationList parameter_list;
			if (ctx.param_decl_list() == None)
				parameter_list = new ParameterDeclarationList(ast,
						new ArrayList<ParameterDeclaration>(), false);
			else
				parameter_list = (ParameterDeclarationList) visit(ctx
						.param_decl_list());
        
        
        if ctx.compound_stmt() == None:
            statement = None
        else:
            statement = visitCompound_stmt(ctx.compound_stmt(), True)
        
        self.ast.call_stack.decrementDepth()
        '''
        '''
            TODO
			Function func = new Function(ast, type, identifier, parameter_list,
					statement, ctx.EXTERN() != null);
        '''
        
        self.ast.symbol_table.decrementScope()
		
        '''
		    TODO
    		return func
    	'''

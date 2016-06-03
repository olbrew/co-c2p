import graphviz as gv

def draw(AST):
    graph = gv.Graph(format='svg')

    visit(AST, graph)

    filename = graph.render(filename='ast')
    
    
def visit(parent, graph):
    if parent.getChildCount() != 0:
        for child in parent.children:
            graph.node(child.getDisplayableText())
            graph.edge(child.getDisplayableText(), parent.getDisplayableText())
            visit(child, graph)
import graphviz as gv

def draw(AST):
    graph = gv.Digraph(format='png')

    labels = {}
    visit(AST, AST.getDisplayableText(), graph, labels)

    filename = graph.render(filename='ast')
    
    
def visit(parentNode, parentName, graph, labels):
    if parentNode.getChildCount() != 0:
        for child in parentNode.children:
            if child.getDisplayableText() in labels.keys():
                labels[child.getDisplayableText()] += 1
            else:
                labels[child.getDisplayableText()] = 1
            childName = child.getDisplayableText()+"_("+str(labels[child.getDisplayableText()])+")"
            
            graph.node(childName)
            graph.edge(parentName, childName)
            visit(child, childName, graph, labels)
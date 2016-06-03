import graphviz as gv


def draw(ast):
    graph = gv.Digraph()

    labels = {}
    visit(ast, ast.getDisplayableText(), graph, labels)

    graph.render('doc/ast.gv', view=True)


def visit(parentNode, parentName, graph, labels):
    if parentNode.getChildCount() != 0:
        for child in parentNode.children:
            if child.getDisplayableText() in labels.keys():
                labels[child.getDisplayableText()] += 1
            else:
                labels[child.getDisplayableText()] = 1
            childName = child.getDisplayableText(
            ) + "_(" + str(labels[child.getDisplayableText()]) + ")"

            graph.node(childName, child.getDisplayableText())
            graph.edge(parentName, childName)
            visit(child, childName, graph, labels)

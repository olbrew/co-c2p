import graphviz as gv


def draw(ast):
    graph = gv.Digraph()

    labels = {}
    visit(ast, graph, labels)

    graph.render('doc/ast.gv', view=True)


def visit(parent, graph, labels):
    if parent.getChildCount() != 0:
        for child in parent.children:

            if child.getDisplayableText() not in labels.keys():
                labels[child.getDisplayableText()] = 1
            else:
                labels[child.getDisplayableText()] += 1

            print(child.getDisplayableText(), labels[
                  child.getDisplayableText()])
            graph.node(str(labels[child.getDisplayableText()]),
                       child.getDisplayableText())
            graph.edge(parent.getDisplayableText(), child.getDisplayableText())

            visit(child, graph, labels)

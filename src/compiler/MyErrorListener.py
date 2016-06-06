from antlr4.error.ErrorListener import ErrorListener


class C2PException(Exception):

    def __init__(self, msg):
        super().__init__()
        self.msg = msg
    
    def __str__(self):
        return self.msg
    

class MyErrorListener(ErrorListener):

    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        exception = str(line) + ":" + str(column) + " " + msg
        raise C2PException("Syntax Error: " + exception)

    def semanticError(self, line, column, msg):
        exception = str(line) + ":" + str(column) + " " + msg
        raise C2PException("Semantic Error: " + exception)

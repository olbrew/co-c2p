from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        exception = str(line) + ":" + str(column) + " " + msg
        raise Exception("Syntax Error: " + exception)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        exception = str(line) + ":" + str(column) + " " + msg
        raise Exception("Ambiguity: " + exception)

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        exception = str(line) + ":" + str(column) + " " + msg
        raise Exception("Attempting Full Context: " + exception)

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        exception = str(line) + ":" + str(column) + " " + msg
        raise Exception("Context Sensitivity: " + exception)
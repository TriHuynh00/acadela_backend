from textx import TextXSyntaxError

class SyntaxErrorHandler():

    def handleSyntaxError(exception):
        print('Syntax Error!!!!, unrecognized command at line', exception.line
              , 'col', exception.col,
              '\n',
              exception.message)
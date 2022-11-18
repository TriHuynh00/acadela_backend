from sacm.exception_handler.syntax_error_handler import keyword_handler


def handle_string_pattern_syntax_errors(exception, expression, line_number):
    error_message = exception.message
    error_line = exception.line
    error_column = exception.col
    # get the line by the line number
    # check if there is only one option
    print("------------------------------------------------")
    print('Syntax Error!, unrecognized command at line', error_line
          , 'col', error_column,
          '\n',
          error_message)
    error_message = keyword_handler.keyword_handler(error_message)
    print(error_message)
    error_message_first = error_message.split("/")[0]

    if "=>" in error_message_first:
        error_message_first = error_message_first.split("=>")[0]

    error_message_last = error_message.split("=>")[1]
    raise Exception(
        #f"Syntax Error! Invalid expression at line {line_number}:\n{expression}! \n "
        f"Syntax Error! Invalid expression at line {line_number}: \n "
        f"{error_message_first} =>{error_message_last}")

from sacm.exception_handler.syntax_error_handler import keyword_handler

def handleSyntaxError(exception, expression, line_number):
    error_message = exception.message
    error_line = exception.line
    error_column = exception.col
    error_file = error_message.split("at position")[1].split(":")[0].replace(" ", "")

    # get the line by the line number
    # check if there is only one option
    print("------------------------------------------------")
    print('Syntax Error!!!!, unrecognized command at line', error_line
          , 'col', error_column,
          '\n',
          error_message)
    error_message = keyword_handler.keyword_handler(error_message)
    print(error_message)
    """ keywords = ['(if)\s','(else if)\s','(else)\s', '(and)\s', '(or)\s', "STRING"]
    replacements = ['if','else if','else', 'and', 'or', "Text with quotes"]
    for index, keyword in enumerate(keywords):
        #print(index,keyword,replacements[index],keyword in error_message)
        error_message = error_message.replace(keyword, replacements[index]) """

    error_message_first = error_message.split("/")[0]
    error_message_last = error_message.split("=>")[1]
    raise Exception(
        "Invalid dynamic field expression: {} found at line {}! \n {} =>{}".format(expression,
                                                                           line_number, error_message_first, error_message_last))

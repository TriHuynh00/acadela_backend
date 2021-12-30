def keyword_handler(error_text):
    # EXPLAIN TECHNICAL TERMS
    keywords_dictionary = {"ID": "identifier(ID)",
                           "STRING": 'Text with quotation marks ("")',
                           "Eq": "Equal sign (=) ",
                           "INT": "Integer (Number)",
                           "STRICTFLOAT":"Number including fraction",
                           "FLOAT": "Number including fraction",
                           "HASH": "Hash sign (#)",
                           "Hash": "Hash sign (#)",
                           "NUMBER": 'Number?',
                           "condition": 'condition(condition is the blabla)?',
                           '(if)\s':"if",
                           '(else if)\s':"else if",
                           '(else)\s':"else", 
                           '(and)\s':"and", 
                           '(or)\s':"or"
                           }
    for word, initial in keywords_dictionary.items():
        error_text = error_text.replace(word, initial)
    error_text = error_text.replace(")\s", "")
    suggestions_init = error_text.split('Expected ')[1]
    suggestions = suggestions_init.split(' or ')
    print(error_text)
    attr_str = 'Expected one of: \n'
    if len(suggestions) == 1:
        error_text = "Expected " + suggestions[0] + '\n'
        return error_text
    else:
        for index, word in enumerate(suggestions):
            attr_str = attr_str + str(index + 1) + '. ' + word + '\n'
        error_text = attr_str
        # EXPLAIN OTHER
        return error_text

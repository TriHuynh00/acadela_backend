def keyword_handler(error_text):
    # EXPLAIN TECHNICAL TERMS
    keywords_dictionary = {"ID": "identifier(ID)",
                           "STRING": 'Text with quotation marks ("", \'\')',
                           "Eq": "Equal sign (=) ",
                           "INT": "Integer (Number)",
                           "STRICTFLOAT":"Number including fraction",
                           "FLOAT": "Number including fraction",
                           "HASH": "Hash sign (#)",
                           "Hash": "Hash sign (#)",
                           "NUMBER": 'Number',
                           "condition": 'condition',
                           '(if)\s':"if",
                           '(else\sif)\s':"else if",
                           '(else)\s':"else", 
                           '(and)\s':"and", 
                           '(or)\s':"or",
                           "WorkspaceTerm":"Workspace",
                           'CaseTerm':"Case",
                           'SettingTerm':"Setting", 
                           'StageTerm':"Stage", 
                           'TaskTerm':"Task",
                            "HumanTaskTerm":"HumanTask",
                            "AutoTaskTerm":"AutoTask",
                            "DualTaskTerm":"DualTask",
                            "FormTerm":"Form",
                            "InputFieldTerm":"InputField",
                            "OutputFieldTerm":"OutputField",
                            "HookTerm":"Hook",
                            "UserTerm":"User",
                            "GroupTerm":"Group",
                            "PreconditionTerm":"Precondition",
                            "FormTerm":"Form",
                            "AttributeTerm":"Attribute"
                           }
    for word, initial in keywords_dictionary.items():
        error_text = error_text.replace(word, initial)
    if "Expected '('" not in error_text:
        error_text = error_text.replace(")\s'", "").replace("'(","")
    suggestions_init = error_text.split('Expected ')[1]
    suggestions = suggestions_init.split(' or ')
    attr_str = 'Expected one of: \n'
    if len(suggestions) == 1:
        error_text = f"Expected {suggestions[0]} \n"
        return error_text
    else:
        for index, word in enumerate(suggestions):
            attr_str = attr_str + str(index + 1) + '. ' + word + '\n'
        error_text = attr_str
        return error_text

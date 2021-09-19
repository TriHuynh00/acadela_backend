from textx import TextXSyntaxError
from . import typo_handler
from . import keyword_handler
import re

def extract_attributes2(metamodel):
    print(" ??")
    namespaces = metamodel.namespaces['CompactTreatmentPlan']
    dictionary = {}
    print("attr_dict", namespaces['GroupIdentity']._tx_attrs)
    for attr in namespaces:
        attr_dict = namespaces[attr]._tx_attrs
        dictionary[attr] = attr_dict.keys()
        if len(attr_dict) != 0:
            print(attr, ':')
            print(attr_dict.keys())
    #print("my dict",dictionary.items())
    return dictionary

def extract_attributes(metamodel):
    namespaces = metamodel.namespaces['CompactTreatmentPlan']
    dictionary = {}
    for attr in namespaces:
        attr_dict = namespaces[attr]._tx_peg_rule
        print(attr,':',attr_dict, type(attr_dict))
        dictionary[attr] = attr_dict
        if type(attr_dict) == 'arpeggio.RegExMatch':
            print(attr, ':')
            print(attr_dict)
    return dictionary

def get_attributes_from_model(meta_model_path):
    f = open(meta_model_path, "r")
    # print(f.read())
    no_whitespace = f.read()
    quotes = re.findall(r'\/\([a-zA-Z]+\)\\s\/|\'[a-zA-Z]+\'', no_whitespace)
    # quotes = re.findall(r'\/\([a-zA-Z]+\)\\s\/', no_whitespace)
    string_list = [each_string.replace(")\s/", "") for each_string in quotes]
    string_list = [each_string.replace("/(", "") for each_string in string_list]
    string_list = [each_string.replace("'", "") for each_string in string_list]
    # print(quotes)
    #print(string_list, len(string_list))
    return string_list

class SyntaxErrorHandler():
    def handleSyntaxError(exception, case_template_str, meta_model_path, model):
        error_message = exception.message
        error_line = exception.line
        error_column = exception.col
        # get the line by the line number
        lines = case_template_str.splitlines()
        print(lines[error_line - 1])
        error_line_str = lines[error_line - 1]
        # check if there is only one option
        print("rulename", exception.expected_rules[0].to_match)
        #print("original error msg: ",error_message)
        rule_name = exception.expected_rules[0].rule_name
        attributes = get_attributes_from_model(meta_model_path)
        #keys = extract_attributes(model)
        keys = extract_attributes2(model)
        print("KEYS\n",keys)
        # if rule_name != '':
        #     error_message = keyword_handler.keyword_handler(error_message)
        # else:
        #     # TYPOS
        #     syntax_error_message = typo_handler.typo_handler(exception, attribute_list, error_line_str)
        #     error_message = keyword_handler.keyword_handler(syntax_error_message)
        # syntax_error_message = typo_handler.typo_handler(exception, attribute_list)
        # error_message = keyword_handler.keyword_handler(syntax_error_message)
        # error_message = error_message.replace(")\s", "").replace("'(", "'")

        syntax_error_message = typo_handler.typo_handler(exception, attributes, error_line_str)
        error_message = keyword_handler.keyword_handler(error_message)
        # error_message = error_message.replace(")\s", "").replace("'(", "'")
        print("------------------------------------------------")
        print('Syntax Error!!!!, unrecognized command at line', error_line
              , 'col', error_column,
              '\n',
              syntax_error_message + error_message)

        # VALIDATING STRING PATTERNS

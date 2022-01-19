import re
from textx import TextXSyntaxError
import os.path
import config.general_config as generalConf
from . import keyword_handler
from . import typo_handler


def extract_attributes2(metamodel):
    namespaces = metamodel.namespaces['CompactTreatmentPlan']
    dictionary = {}
    for attr in namespaces:
        attr_dict = namespaces[attr]._tx_attrs
        dictionary[attr] = attr_dict.keys()
    return dictionary


def extract_attributes(metamodel):
    namespaces = metamodel.namespaces['CompactTreatmentPlan']
    dictionary = {}
    for attr in namespaces:
        attr_dict = namespaces[attr]._tx_peg_rule
        print(attr, ':', attr_dict, type(attr_dict))
        dictionary[attr] = attr_dict
        if type(attr_dict) == 'arpeggio.RegExMatch':
            print(attr, ':')
            print(attr_dict)
    return dictionary


def get_attributes_from_model(meta_model_path):
    f = open(meta_model_path, "r")
    # print(f.read())
    no_whitespace = f.read()
    # add double quotes as well
    quotes = re.findall(r'\/\([a-zA-Z]+\)\\s\/|\'[a-zA-Z]+\'', no_whitespace)
    # quotes = re.findall(r'\/\([a-zA-Z]+\)\\s\/', no_whitespace)
    string_list = [each_string.replace(")\s/", "") for each_string in quotes]
    string_list = [each_string.replace("/(", "") for each_string in string_list]
    string_list = [each_string.replace("'", "") for each_string in string_list]
    # print(quotes)
    # print(string_list, len(string_list))
    return string_list


def get_hash_attributes(meta_model_path):
    f = open(meta_model_path, "r")
    grammar = f.read()
    quotes = re.split('Hash', grammar)
    hash_keywords = []
    for quote in quotes[1:]:
        end = re.search('#', quote)
        if end:
            break
        word = re.split('\)\s\;', quote)
        word = re.sub(r'\s+', '', word[0])
        quoted_attrs = re.findall(r'\|\'[a-zA-Z]+\'|\(\'[a-zA-Z]+\'', word)
        not_quoted_attrs = re.findall(r'\|[a-zA-Z]+|\([a-zA-Z]+', word)
        quoted_attrs = [each_string.replace("(", "").replace("|", "").replace("'", "") for each_string in quoted_attrs]
        not_quoted_attrs = [each_string.replace("(", "").replace("|", "") for each_string in not_quoted_attrs]
        extracted_keywords = []

        for attr in not_quoted_attrs:
            attr_regex = re.escape(attr) + r"\:\s+\'(.+?)\'"
            extracted = re.findall(attr_regex, grammar)
            print("extracted keywords:", extracted)
            extracted_keywords = extracted_keywords + [extracted[0].replace("'", "")]
            # if len(extracted)>0:
            # extracted = re.findall(r'\'[a-zA-Z]+\'', extracted[0])
            # print ("extracted keywords:",extracted)
            # extracted_keywords = extracted_keywords + [extracted[0].replace("'", "")]
        hash_keywords = hash_keywords + quoted_attrs + extracted_keywords
    print("keywords", hash_keywords)
    return hash_keywords


class SyntaxErrorHandler():
    def handleSyntaxError(exception, case_template_str, meta_model_path, model):
        error_message = exception.message
        error_line = exception.line
        error_column = exception.col
        error_file = error_message.split("at position")[1].split(":")[0].replace(" ", "")
        is_file_exists = os.path.isfile(error_file)
        print("error file", error_file)
        if error_file is not None and generalConf.MODEL_PLACEHOLDER in error_file:
            lines = case_template_str.splitlines()
        elif is_file_exists:
            f = open(error_file, "r")
            error_file_text = f.read()
            print("error message", error_file, error_file_text)
            lines = error_file_text.splitlines()

        # get the line by the line number
        print(lines[error_line - 1])
        error_line_str = lines[error_line - 1]
        # check if there is only one option
        print("rulename", exception.__dict__)
        # print("original error msg: ",error_message)
        rule_name = exception.expected_rules[0].rule_name
        print("EXCEPTION", exception.expected_rules[0].__dict__)
        # handle number (0-0)
        # handle missing dot '.'

        if rule_name == 'Eq' or rule_name == 'STRING'or rule_name == 'INT':
            error_message = keyword_handler.keyword_handler(error_message)
            print(error_message)
            raise Exception(  "Syntax Error!! Unrecognized command at line {} and column {}!\n{} ".format(error_line, error_column,  error_message ))
            return
        attributes = get_attributes_from_model(meta_model_path)
        hash_attributes = get_hash_attributes(meta_model_path)
        # keys = extract_attributes(model)
        #keys = extract_attributes2(model)
        # if rule_name != '':
        #     error_message = keyword_handler.keyword_handler(error_message)
        # else:
        #     # TYPOS
        #     syntax_error_message = typo_handler.typo_handler(exception, attribute_list, error_line_str)
        #     error_message = keyword_handler.keyword_handler(syntax_error_message)
        # syntax_error_message = typo_handler.typo_handler(exception, attribute_list)
        # error_message = keyword_handler.keyword_handler(syntax_error_message)
        # error_message = error_message.replace(")\s", "").replace("'(", "'")

        syntax_error_message = typo_handler.typo_handler(exception, attributes, hash_attributes, error_line_str)
        error_message = keyword_handler.keyword_handler(error_message)
        # error_message = error_message.replace(")\s", "").replace("'(", "'")
        print("------------------------------------------------")
        raise Exception(  "Syntax Error!! Unrecognized command at line {} and column {}!\n{} ".format(error_line, error_column, syntax_error_message + error_message ))

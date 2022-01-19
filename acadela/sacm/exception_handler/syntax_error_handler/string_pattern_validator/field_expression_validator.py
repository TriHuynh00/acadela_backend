import re
from os.path import join, dirname, abspath
from . import util
from textx import *
from . import syntax_error_handler


def validate_expression(expression, line_number):
    print("the if-else expression:", expression)
    this_folder = dirname(__file__)
    # there has to be () and CompareExpression or ParamPattern in between
    # compare expression --> NUMBER (Comparator ColorName Comparator NUMBER)+
    if expression.startswith("if"):
        #expression = expression.replace(" ", "")
        try:
            meta_model_path = join(this_folder, 'grammars','if_else_expression.tx')
            mm = metamodel_from_file(meta_model_path,
                                        ignore_case=True)
            if_else_meta = mm.model_from_str(expression, meta_model_path)
        except TextXSyntaxError as e:
            syntax_error_handler.handleSyntaxError(e, expression, line_number)
        print(expression)
        expression = expression.replace(" ", "")
        regex_compare_expression = re.compile(r'if\([a-zA-Z]+(=|<>|<=|>=|<|>)[0-9]+((and|or)[a-zA-Z]+('
                                              r'=|<>|<=|>=|<|>)[0-9]+)*\)then\"[a-zA-Z]+\"(elseif\([a-zA-Z]+('
                                              r'=|<>|<=|>=|<|>)[0-9]+((and|or)[a-zA-Z]+( '
                                              r'=|<>|<=|>=|<|>)[0-9]+)*\)then\"['
                                              r'a-zA-Z]+\")*else\"[a-zA-Z]+\"', re.I)
        match_if_else = regex_compare_expression.match(expression)
        print("does it match?", bool(match_if_else))
        return bool(match_if_else)
    elif expression.startswith("round"):
        print("handle round")
        round_count = expression.count("round")
        print("round count:",round_count)
        try:
            meta_model_path = join(this_folder, 'grammars', 'round_expression.tx')
            mm = metamodel_from_file(meta_model_path,
                                     ignore_case=True)
            print("before split",expression)
            if round_count == 2:
                expression = expression.split("round(", 1)[1][:-1]
            print("expression:", expression)
            expression_meta = mm.model_from_str(expression, meta_model_path)
        except TextXSyntaxError as e:
            syntax_error_handler.handleSyntaxError(e, expression, line_number)
        return True
    return True

    # implement round validation


def validate_field_expressions(case_object_tree, treatment_str):
    print("------------------------------------------------")
    task_list = case_object_tree["tasks"]
    for task in task_list:
        dynamic_task_fields = task.dynamicFieldList
        if len(dynamic_task_fields) > 0:
            for field in dynamic_task_fields:
                if field.expression:
                    line_number = util.find_line_number(treatment_str, field, 'expression')
                    is_valid = validate_expression(field.expression, line_number)
                    if not is_valid:
                        raise Exception(
                            "Invalid dynamic field expression: {} \n found at line {}!".format(field.expression,
                                                                                               line_number))
import re
from . import util
from textx import *
from os.path import join, dirname, abspath
from . import string_pattern_syntax_error_handler

def validate_ref_text(ui_ref, line_number):
    print("the uiRef:", ui_ref)
    this_folder = dirname(__file__)
    try:
        meta_model_path = join(this_folder, 'grammars','ui_ref.tx')
        mm = metamodel_from_file(meta_model_path, ignore_case=True)
        ui_ref_meta = mm.model_from_str(ui_ref, meta_model_path)
    except TextXSyntaxError as e:
        string_pattern_syntax_error_handler.handle_string_pattern_syntax_errors(e, ui_ref, line_number)
        
    # if ui_ref == 'privatelink' or ui_ref == 'hidden':
    #     return True
    # else:
    #     print("check if the color function is valid")
    #     if not ui_ref.startswith("colors"):
    #         print("function name incorrect")
    #         return False
        # there has to be () and CompareExpression or ParamPattern in between
        # compare expression --> NUMBER (Comparator ColorName Comparator NUMBER)+
        # regex_compare_expression = re.compile(
        #     r'colors\([0-9]+((=|<>|<=|>=|<|>)(red|blue|green|orange|yellow)(=|<>|<=|>=|<|>)[0-9]+)+\)', re.MULTILINE)
        # match_compare = regex_compare_expression.match(ui_ref)
        # print("?", bool(match_compare))
        # return bool(match_compare)
        # ParamPattern --> Text (',' Text)* ?? SHOULD I DO THIS?
        # regex_param_pattern = re.compile(r'\([a-zA-Z]+[[a-zA-Z]+]*\)', re.I)
        # match_param = regex.regex_param_pattern(ui_ref)
        # print("??", bool(match_param))

def validate_field_ui_ref(field, treatment_str):
    line_number = util.find_line_number(treatment_str, field, 'uiRef')
    validate_ref_text(field.uiReference, line_number)

def validate_ui_ref(case_object_tree, treatment_str):
    print("------------------------------------------------")
    task_list = case_object_tree["tasks"]
    for task in task_list:
        dynamic_fields = task.dynamicFieldList
        if len(dynamic_fields) > 0:
            for field in dynamic_fields:
                if field.uiReference:
                    line_number = util.find_line_number(treatment_str, field, 'uiRef')
                    validate_ref_text(field.uiReference, line_number)

        fields = task.fieldList
        if len(fields) > 0:
            for field in fields:
                if field.uiReference:
                    line_number = util.find_line_number(treatment_str, field, 'uiRef')
                    validate_ref_text(field.uiReference, line_number)

